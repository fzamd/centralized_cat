import os

import argparse
import shlex
from pymarc import MARCReader

from centralized_cat import settings
from cat_backend.models import Record, Source


def _get_marc_data(folder_path, resource_id):
    with open(folder_path + '/bib-' + str(resource_id) + '.marcstd', 'rb') as data:
        reader = MARCReader(data)
        for record in reader:
            return record


def _fetch_sources():
    return Source.objects.all()


def _get_last_record(source_id):
    return Record.objects.filter(source__id=source_id).count()


def _insert_data_to_db(folder_path, source, resource_id, dry_run):
    marc_data = _get_marc_data(folder_path, resource_id)

    try:
        record = Record.objects.get(isbn=marc_data.isbn())
        print('Record already exists', {'record_id': record.id, 'isbn': record.isbn()})
        if not dry_run:
            record.source.add(source)
    except Exception as err:
        record = Record(
            title=marc_data.title(),
            subtitle='',
            isbn=marc_data.isbn(),
            edition=int(marc_data['250'].value()[:1]) if marc_data['250'] else 1,
            publisher=marc_data.publisher(),
            publish_year=marc_data.pubyear()[1:5] if marc_data.pubyear() else None,
            author=marc_data.author() if marc_data.author() else None,
            source_bib_id=resource_id,
            source_control_id=marc_data['001'].value() if marc_data['001'] else None,
            item_type='book'
        )

        if not dry_run:
            record.save()
            record.source.add(source)

    print('Saved record to DB:', {'title': record.title, 'isbn': record.isbn})


def populate_data_in_db(dry_run=True, sources=[]):
    lookup_sources = _fetch_sources()
    if len(sources):
        lookup_sources = [source for source in lookup_sources if source.short_form in sources]

    for source in lookup_sources:
        source_folder_path = str(settings.BASE_DIR) + '/raw_data/' + source.short_form
        num_of_resources = len(os.listdir(source_folder_path)) - 1
        starting_resource_id = _get_last_record(source.id) if _get_last_record(source.id) else 1
        for resource_id in range(starting_resource_id, num_of_resources):
            try:
                _insert_data_to_db(source_folder_path, source.id, resource_id, dry_run)
            except Exception as err:
                print('Error storing data to DB', {'resource_id': resource_id, 'source': source.name, err: str(err)})


def run(*args):
    dry_run = True
    sources = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", type=str)
    parser.add_argument("--sources", type=str)

    try:
        split_args = shlex.split(args[0])
    except IndexError:
        split_args = []

    args2 = parser.parse_args(split_args)
    if args2.dry_run:
        dry_run = 'false' not in args2.dry_run and 'False' not in args2.dry_run

    if args2.sources:
        sources = args2.sources.split(' ')

    populate_data_in_db(dry_run, sources)


if __name__ == "__main__":
    run()

""" Fetch Library MARC
This script fetches records from different library specified in the db source.

Usage:
    python manage.py runscript fetch_library_marc --script-args="--dry-run=false"
"""
import os
import re
import json
from datetime import datetime

import requests
import argparse
import shlex

from cat_backend.models import Source
from centralized_cat import settings


def _get_marc_data(source, resource_id):
    print('Fetching data for record: ', resource_id)
    query_params = {
        'op': 'export',
        'format': 'marcstd',
        'bib': resource_id
    }
    response = requests.get(source.opac_domain + source.resource_url, params=query_params)
    response.raise_for_status()

    file_name_from_header = re.findall('filename="(.+)"', response.headers['content-disposition'])
    file_name = file_name_from_header[0] if len(file_name_from_header) else 'bib-' + resource_id

    return response.text, file_name


def _get_resume_info(folder_path, re_fetch):
    resource_id = 1

    if not re_fetch:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        resume_data = {}
        try:
            with open(folder_path + '/resume_config.json', 'r') as fp:
                resume_data = json.loads(fp.read())
        except Exception as err:
            print('Error while reading resume config', {err: str(err)})

        if bool(resume_data):
            resource_id = resume_data['resume_from']

    return resource_id


def _save_marc_file(folder_path, file_name, resource_id, marc_data, dry_run):
    if dry_run:
        print('Saved record data to file', {'file_name': file_name, 'record_id': resource_id, 'marc_data': marc_data})
    else:
        with open(folder_path + '/' + file_name, 'w') as fp:
            fp.write(marc_data + '\n')
        with open(folder_path + '/' + 'resume_config.json', 'w') as fp:
            fp.write(json.dumps({'resume_from': resource_id + 1, 'last_ran': datetime.utcnow().isoformat()}))
        print('Saved record data to file', {'file_name': file_name, 'resource_id': resource_id})


def _fetch_sources():
    return Source.objects.all()


def fetch_record_from_sources(dry_run=True, re_fetch=False, sources=[]):
    lookup_sources = _fetch_sources()
    if len(sources):
        lookup_sources = [source for source in lookup_sources if source.short_form in sources]

    for source in lookup_sources:
        print('Fetching data from source: ', source.name)
        print('-----')
        folder_path = str(settings.BASE_DIR) + '/raw_data/' + source.short_form
        resource_id = _get_resume_info(folder_path, re_fetch)
        fail_count = 0
        while fail_count < 3:
            try:
                marc_data, file_name = _get_marc_data(source, resource_id)
            except requests.exceptions.HTTPError as err:
                print('Exception occurred while fetching record',
                      {'resource_id': resource_id, 'url': source.opac_domain + source.resource_url, err: str(err)})
                fail_count += 1
                continue

            try:
                _save_marc_file(folder_path, file_name, resource_id, marc_data, dry_run)
            except Exception as err:
                print('Error while writing raw_data to file',
                      {'folder_path': folder_path, 'file_name': file_name, 'err': str(err)})

            resource_id += 1


def run(*args):
    dry_run = True
    re_fetch = False
    sources = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", type=str)
    parser.add_argument("--re-fetch", type=str)
    parser.add_argument("--sources", type=str)

    try:
        split_args = shlex.split(args[0])
    except IndexError:
        split_args = []

    args2 = parser.parse_args(split_args)
    if args2.dry_run:
        dry_run = 'false' not in args2.dry_run and 'False' not in args2.dry_run

    if args2.re_fetch:
        re_fetch = 'true' in args2.re_fetch or 'True' in args2.re_fetch

    if args2.sources:
        sources = args2.sources.split(' ')

    fetch_record_from_sources(dry_run, re_fetch, sources)


if __name__ == "__main__":
    run()

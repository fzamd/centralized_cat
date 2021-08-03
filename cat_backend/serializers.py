from cat_backend.models import Record, Source
from rest_framework import serializers


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'title', 'subtitle', 'author', 'publisher', 'publish_year', 'item_type']


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'short_form', 'name', 'opac_domain', 'resource_url']

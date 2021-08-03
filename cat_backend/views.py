from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from cat_backend.serializers import RecordSerializer, SourceSerializer
from cat_backend.models import Record, Source


class ResultSetPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    max_page_size = 1000


class RecordViewSet(viewsets.ModelViewSet):

    queryset = Record.objects.all().order_by('id')
    serializer_class = RecordSerializer
    pagination_class = ResultSetPagination


class SourceViewSet(viewsets.ModelViewSet):

    queryset = Source.objects.all().order_by('id')
    serializer_class = SourceSerializer
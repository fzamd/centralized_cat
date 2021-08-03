from django.db import models
from datetime import datetime


class Source(models.Model):
    institution = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    opac_domain = models.CharField(max_length=200)
    resource_url = models.CharField(max_length=200)
    short_form = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Record(models.Model):
    author = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=datetime.utcnow())
    edition = models.IntegerField(null=True)
    isbn = models.CharField(max_length=13)
    item_type = models.CharField(max_length=20)
    publisher = models.CharField(max_length=100)
    publish_year = models.IntegerField(null=True)
    source = models.ManyToManyField(Source)
    source_bib_id = models.IntegerField()
    source_control_id = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=1000)
    thumbnail = models.URLField()
    title = models.CharField(max_length=500)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

import os
from django.db import models

from base import settings


def upload_to(instance, filename):
    base, extension = os.path.splitext(filename.lower())
    return f'users/{instance.document.owner}/{base}.{str(instance.index)}{extension}'


class Document(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=2048, blank=True, default='', unique=True)
    owner = models.ForeignKey('auth.User', related_name='documents', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)


class Revision(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=True, upload_to=upload_to)
    document = models.ForeignKey('versioning.Document', related_name='revisions', on_delete=models.CASCADE)
    revision_url = models.CharField(max_length=2048, blank=True)
    index = models.IntegerField(blank=True, default=0)

    @property
    def url(self):
        return self.file.name

    @property
    def document_url(self):
        return self.document.url

    @property
    def document_owner(self):
        return self.document.owner

    def get_index(self):
        return self.document.revisions.count()

    def get_revision_url(self):
        return self.document.url + '?revision=' + str(self.get_index())

    def save(self, *args, **kwargs):
        self.index = self.get_index()
        self.revision_url = self.get_revision_url()
        super(Revision, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)



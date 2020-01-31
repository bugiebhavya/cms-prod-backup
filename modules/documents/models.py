from django.db import models
from wagtail.documents.models import Document, AbstractDocument
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save 
from wagtailvideos.models import Channels
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
import os
from datetime import datetime
"""
Preview generator:
# https://pypi.org/project/preview-generator-ivc/
# https://pypi.org/project/preview-generator/
"""
from preview_generator.manager import PreviewManager
from django.core.files.base import File

class Area(models.Model):
    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Area')
        ordering = ('name',)

    name = models.CharField(max_length=100, verbose_name=_('Area name'))
    notes = models.TextField(verbose_name=_('Notes'), default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Subject(models.Model):
    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subject')
        ordering = ('name',)

    name = models.CharField(max_length=100, verbose_name=_('Subject name'))
    notes = models.TextField(verbose_name=_('Notes'), default="")
    area = models.ForeignKey(Area, verbose_name=_('Area'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class Topic(models.Model):
    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topic')
        ordering = ('name',)

    name = models.CharField(max_length=100, verbose_name=_('Topic name'))
    notes = models.TextField(verbose_name=_('Notes'), default="")
    subject = models.ForeignKey(Subject, verbose_name=_('Subject'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class SubTopic(models.Model):
    class Meta:
        verbose_name = _('SubTopic')
        verbose_name_plural = _('SubTopic')
        ordering = ('name',)
    name = models.CharField(max_length=100, verbose_name=_('Subtopic name'))
    notes = models.TextField(verbose_name=_('Notes'), default="")
    topic = models.ForeignKey(Topic,  verbose_name=_('Topic'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class Natures(models.Model):
    class Meta:
        verbose_name = _('Nature')
        verbose_name_plural = _('Nature')
        ordering = ('name',)
    name = models.CharField(max_length=100, verbose_name=_('Nature name'))
    notes = models.TextField(verbose_name=_('Notes'), default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)



class CustomDocument(AbstractDocument):
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
    SCOPE = (
        (PUBLIC, _('Public')),
        (PRIVATE, _('Private')),)
    area = models.ForeignKey(Area, related_name="area_documents", verbose_name=_('Area'), on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, related_name="subject_documents", verbose_name=_('Subject'), on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(Topic, related_name="topic_documents", verbose_name=_('Topic'), on_delete=models.SET_NULL, null=True, blank=True)
    subtopic = models.ForeignKey(SubTopic, related_name="subtopic_documents", verbose_name=_('SubTopic'), on_delete=models.SET_NULL, null=True, blank=True)
    nature = models.ForeignKey(Natures, related_name="nature_documents", verbose_name=_('Natures'), on_delete=models.SET_NULL, null=True, blank=True)
    favorites = GenericRelation("users.Favorite", related_query_name='fav_documents')
    comments = GenericRelation("home.Comment", related_query_name='comments')
    media_views = GenericRelation("dashboard.MediaView", related_query_name='document_media_views')
    thumbnail = models.FileField(upload_to='documents', blank=True, verbose_name=('thumbnail'), default='documents/logo.png')
    access = models.CharField(verbose_name=('Access Type'), default="PUBLIC", choices=SCOPE, max_length=50, blank=True, null=True)
    channel = models.ForeignKey(Channels, related_name="documents", on_delete=models.SET_NULL, null=True, blank=True)
    # new fields
    author = models.CharField(max_length=100, verbose_name=_('Author'),  null=True, blank=True)
    author_profession = models.CharField(max_length=200, verbose_name=_('Author Profession'),  null=True, blank=True)
    validity_start = models.DateField(verbose_name=_('Validity Start'), default=datetime.now, null=True, blank=True)
    validity_end = models.DateField(verbose_name=_('Validity End'), default=datetime.now, null=True, blank=True)
    synthesis = models.TextField(verbose_name=_('Synthesis'), default="", null=True, blank=True)
    publication_at = models.DateTimeField(verbose_name=_('Publish At'), default=datetime.now, null=True, blank=True)
    expiration_at = models.DateField(verbose_name=_('Publish End'), default=datetime.now, null=True, blank=True)
    republication_at = models.DateTimeField(verbose_name=_('Republish At'), default=datetime.now, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True, db_index=True)

    admin_form_fields = (
        'channel',
        'title',
         'area',
        'subject',
        'topic',
        'subtopic',
        'nature',
        'file',
        'collection',
        'tags',
        'thumbnail',
        'access',
        'author',
        'author_profession',
        'validity_start',
        'validity_end',
        'synthesis',
        'publication_at',
        'expiration_at',
        'republication_at',
    )


def add_thumbnail(sender, instance, created, **kwargs):
    if created:
        if instance.file.name.split('.')[-1] in ['ppt', 'pptx', 'doc', 'docx', 'xls', 'xlsx', 'pdf']:
            cache_path = '/tmp/preview_cache'
            file_to_preview_path = instance.file.path
            manager = PreviewManager(cache_path, create_folder= True)
            print(file_to_preview_path)
            doc_path = manager.get_jpeg_preview(file_to_preview_path, width=300, height=400)
            instance.thumbnail.save(os.path.basename(doc_path), File(open(doc_path, 'rb')), save=True)
            os.remove(doc_path)
        else:
            instance.delete()

post_save.connect(add_thumbnail, CustomDocument)
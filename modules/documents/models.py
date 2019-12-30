from django.db import models
from wagtail.documents.models import Document, AbstractDocument
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save 
from wagtailvideos.models import Channels
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
import os
from preview_generator.manager import PreviewManager
from django.core.files.base import File


class CustomDocument(AbstractDocument):
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
    SCOPE = (
        (PUBLIC, _('Public')),
        (PRIVATE, _('Private')),)

    comments = GenericRelation("home.Comment", related_query_name='comments')
    media_views = GenericRelation("dashboard.MediaView", related_query_name='media_views')
    thumbnail = models.FileField(upload_to='documents', blank=True, verbose_name=('thumbnail'), default='documents/logo.png')
    access = models.CharField(verbose_name=('Access Type'), default="PUBLIC", choices=SCOPE, max_length=50, blank=True, null=True)
    channel = models.ForeignKey(Channels, related_name="documents", on_delete=models.SET_NULL, null=True, blank=True)

    admin_form_fields = (
        'channel',
        'title',
        'file',
        'collection',
        'tags',
        'thumbnail',
        'access',
    )

    
    def update_views(self):
        if self.media_views.exists():
            obj = self.media_views.last()
            obj.views +=1
            obj.save()
        else:
            from modules.dashboard.models import MediaView
            obj = MediaView(content_object=self, views=0)
            obj.views = 1
            obj.save()

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
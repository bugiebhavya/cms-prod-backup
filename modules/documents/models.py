from django.db import models
from wagtail.documents.models import Document, AbstractDocument
from django.dispatch import receiver
from django.db.models.signals import post_delete 
from wagtailvideos.models import Channels
# Create your models here.
from django.contrib.contenttypes.fields import GenericRelation

ACCESS = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),

    )
class CustomDocument(AbstractDocument):
    comments = GenericRelation("home.Comment", related_query_name='comments')
    thumbnail = models.FileField(upload_to='documents', blank=True, verbose_name=('thumbnail'), default='documents/logo.png')
    access = models.CharField(verbose_name=('Access Type'), default="PUBLIC", choices=ACCESS, max_length=50, blank=True, null=True)
    channel = models.ForeignKey(Channels, related_name="documents", on_delete=models.CASCADE)

    admin_form_fields = (
        'channel',
        'title',
        'file',
        'collection',
        'tags',
        'thumbnail',
        'access',
    )

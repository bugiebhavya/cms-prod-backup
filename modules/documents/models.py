from django.db import models
from wagtail.documents.models import Document, AbstractDocument
from django.dispatch import receiver
from django.db.models.signals import post_delete 
from wagtailvideos.models import Channels
# Create your models here.


ACCESS = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),

    )
class CustomDocument(AbstractDocument):
    thumbnail = models.FileField(upload_to='documents', blank=True, verbose_name=('thumbnail'), default='documents/logo.png')
    access = models.CharField(verbose_name=('Access Type'), default="PUBLIC", choices=ACCESS, max_length=50, blank=True, null=True)
    

    admin_form_fields = (
        'title',
        'file',
        'collection',
        'tags',
        'thumbnail',
        'access'
    )

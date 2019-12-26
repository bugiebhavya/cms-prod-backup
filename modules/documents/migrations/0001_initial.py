# Generated by Django 2.2.8 on 2019-12-23 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.core.models
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.FileField(upload_to='documents', verbose_name='file')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('file_hash', models.CharField(blank=True, editable=False, max_length=40)),
                ('thumbnail', models.FileField(blank=True, default='documents/logo.png', upload_to='documents', verbose_name='thumbnail')),
                ('access', models.CharField(blank=True, choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], default='PUBLIC', max_length=50, null=True, verbose_name='Access Type')),
                ('collection', models.ForeignKey(default=wagtail.core.models.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Collection', verbose_name='collection')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
                'abstract': False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
    ]
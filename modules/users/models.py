from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
import pdb, os
from unidecode import unidecode
from django.db.models.signals import post_save
from django.dispatch import receiver

def get_expiry_date():
	return datetime.now()+timedelta(days=30)

class AssociateSector(models.Model):
    class Meta:
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')
    value = models.CharField(verbose_name=_('Value'),max_length=150, unique=True)
    notes = models.TextField(verbose_name=_('Notes'), default="", blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return mark_safe(self.value)

class AssociatesLevel(models.Model):
    class Meta:
        verbose_name = _('Associate Level')
        verbose_name_plural = _('Associate Levels')
    title = models.CharField(verbose_name=_('Level Title'),max_length=100, unique=True)
    allowed_users = models.PositiveIntegerField(default=0, verbose_name=_('Allowed users'))
    access = models.PositiveIntegerField(default=0, verbose_name=_('Access'), help_text=_('Number of access allowed'))
    consults = models.PositiveIntegerField(default=0, verbose_name=_('Consults'), help_text=_('Number of media User can view'))
    download = models.PositiveIntegerField(default=0, verbose_name=_('Downloads'), help_text=_('Number of media User can download'))
    notes = models.TextField(verbose_name=_('Notes'), default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return mark_safe('{0}   (Usuarios: {1})'.format(self.title, self.allowed_users))

class Society(models.Model):
    class Meta:
        verbose_name = _('Society')
        verbose_name_plural = _('Society')
    title = models.CharField(verbose_name=_('Name'),max_length=100, unique=True)
    notes = models.TextField(verbose_name=_('Notes'), default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Associate(models.Model):
    class Meta:
        verbose_name = _('Associate')
        verbose_name_plural = _('Associate')
    company = models.CharField(verbose_name=_('Company Name'),max_length=100, unique=True)
    rfc = models.CharField(verbose_name=_('RFC'),max_length=100, unique=True)
    address = models.CharField(verbose_name=_('Address'), max_length=200)
    tax_residence = models.CharField(verbose_name=_('Tax residence'), max_length=100)
    state = models.CharField(verbose_name=_('State'), max_length=100)
    sociaty = models.ForeignKey(Society, verbose_name=_('Society'), on_delete=models.SET_NULL, null=True)

    legal_representative = models.CharField(verbose_name=_('Legal representative'), max_length=100)
    membership_start = models.DateField(verbose_name=_('Membership Start Date'), default=datetime.now)
    membership_end = models.DateField(verbose_name=_('Membership End Date'), default=get_expiry_date, null=True, blank=True)
    sector = models.ForeignKey(AssociateSector, verbose_name=_('Sector'), on_delete=models.SET_NULL, null=True, blank=True)
    web_page = models.URLField(verbose_name=_('Web page'), max_length=200, blank=True, null=True)
    email = models.CharField(verbose_name=_('Email address'), max_length=200, unique=True)
    associate_level = models.ForeignKey(AssociatesLevel, verbose_name=_('Level of associate'), on_delete=models.SET_NULL, null=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.company)

def get_upload_to(instance, filename):
    """
    Obtain a valid upload path for an image file.

    This needs to be a module-level function so that it can be referenced within migrations,
    but simply delegates to the `get_upload_to` method of the instance, so that AbstractImage
    subclasses can override it.
    """
    return instance.get_upload_to(filename)

class UserInterest(models.Model):
    """docstring for UserInterest"""
    class Meta:
        verbose_name = _('Interest')
        verbose_name_plural = _('Interest')
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=100)
    def __str__(self):
        return self.name

@receiver(post_save, sender=UserInterest)
def craeteEmptyInterests(sender, instance, **kwargs):
    o = User.objects.all()
    createList = []
    for i in o:
        createList.append(UserInterestPercent(interest=instance,user=i,percent = 0))
    UserInterestPercent.objects.bulk_create(createList)    

    
        
class User(AbstractUser):
    class Meta:
        ordering = ('-last_name',)
    associate = models.ForeignKey(Associate, verbose_name=_('Associate'), on_delete=models.SET_NULL, null=True, blank=True)
    position_held = models.CharField(verbose_name=_('Position held'), max_length=100, null=True, blank=True)
    download_remain = models.PositiveIntegerField(default=0, verbose_name=_('Downloads remain'), help_text=_('Number of media User can download'))
    profile_image = models.ImageField( verbose_name=_('Profile Image'), upload_to=get_upload_to)
    intrests = models.ManyToManyField(UserInterest, blank=True, verbose_name=_('Interest'))
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    report_access = models.BooleanField(verbose_name=_('Report Access'), default=False)

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if self._state.adding:
            try:
                self.download_remain = self.associate.associate_level.download
            except:
                pass
        return super(User, self).save(*args, **kwargs)

    def clean(self):
        if self._state.adding:
            associate = self.associate
            if associate and associate.user_set.all().count() > associate.associate_level.allowed_users:
                raise ValidationError(_("Max allowed users reached for that membership"))

    @property
    def can_download(self):
        return self.download_remain > 0

    @property
    def user_role_name(self):
        return ",".join(self.groups.values_list('name', flat=True))

    def get_upload_to(self, filename):
        folder_name = 'profile_images'
        filename = self.profile_image.field.storage.get_valid_name(filename)

        # do a unidecode in the filename and then
        # replace non-ascii characters in filename with _ , to sidestep issues with filesystem encoding
        filename = "".join((i if ord(i) < 128 else '_') for i in unidecode(filename))

        # Truncate filename so it fits in the 100 character limit
        # https://code.djangoproject.com/ticket/9893
        full_path = os.path.join(folder_name, filename)
        if len(full_path) >= 95:
            chars_to_trim = len(full_path) - 94
            prefix, extension = os.path.splitext(filename)
            filename = prefix[:-chars_to_trim] + extension
            full_path = os.path.join(folder_name, filename)

        return full_path

class UserInterestPercent(models.Model):
    class Meta:
        ordering = ('interest',)
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name=_('User'), null = True)
    interest = models.ForeignKey(UserInterest, on_delete=models.CASCADE, verbose_name=_('Interest'), null = False)
    percent = models.IntegerField(null = False, max_length=3)

    

class Favorite(models.Model):
    """ Represents an instance of Favorite """
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, null=True, blank=True,  on_delete=models.CASCADE,)
    cookie = models.CharField(null=True, max_length=256, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.user.username)

class UserLog(models.Model):
    class Meta:
        verbose_name = _('User Log')
        verbose_name_plural = _('User Logs')
    action_types = [
    ('LOGIN', _('LOGIN')),
    ('CONSULT MEDIA', _('CONSULT MEDIA')),
    ('DOWNLOAD MEDIA', _('DOWNLOaD MEDIA')),
]
    action = models.CharField(verbose_name=('Action Type'), choices=action_types, max_length=50, blank=False, null=False)
    username = models.CharField(verbose_name=_('Username'), blank=False, null=False, max_length=50)
    date = models.DateField(verbose_name=_('Date'), null=False, auto_now_add=True)
    time = models.TimeField(verbose_name=_('Date'), null=False, auto_now_add=True)
    media = models.CharField(verbose_name=_('Media'), blank=True, null=True, max_length=80)
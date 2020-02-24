from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe

def get_expiry_date():
	return datetime.now()+timedelta(days=30)

class AssociatesLevel(models.Model):
    class Meta:
        verbose_name = _('Associate Level')
        verbose_name_plural = _('Associate Levels')
    title = models.CharField(verbose_name=_('Level Title'),max_length=100, unique=True)
    allowed_users = models.PositiveIntegerField(default=0, verbose_name=_('Allowed users'))
    notes = models.TextField(verbose_name=_('Notes'), default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return mark_safe('{0}   (Usuarios: {1})'.format(self.title, self.allowed_users))


class Associate(models.Model):
    class Meta:
        verbose_name = _('Associate')
        verbose_name_plural = _('Associate')
    rfc = models.CharField(verbose_name=_('RFC'),max_length=100, unique=True)
    tax_residence = models.CharField(verbose_name=_('Tax residence'), max_length=100)
    state = models.CharField(verbose_name=_('State'), max_length=100)
    sociaty = models.CharField(verbose_name=_('Sociaty'), max_length=200)
    legal_representative = models.CharField(verbose_name=_('Legal representative'), max_length=100)
    membership_start = models.DateField(verbose_name=_('Membership Start Date'), default=datetime.now)
    membership_end = models.DateField(verbose_name=_('Membership End Date'), default=get_expiry_date)
    sector = models.CharField(verbose_name=_('Sector'), max_length=200)
    web_page = models.URLField(verbose_name=_('Web page'), max_length=200)
    email = models.CharField(verbose_name=_('Email address'), max_length=200, unique=True)
    associate_level = models.ForeignKey(AssociatesLevel, verbose_name=_('Level of associate'), on_delete=models.SET_NULL, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rfc)

class User(AbstractUser):
    associate = models.ForeignKey(Associate, verbose_name=_('Associate'), on_delete=models.SET_NULL, null=True, blank=True)
    position_held = models.CharField(verbose_name=_('Position held'), max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.username)

    def clean(self):
        associate = self.associate
        if associate.user_set.all().count() >= associate.associate_level.allowed_users:
            raise ValidationError(_("Max allowed users reached for that membership"))


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
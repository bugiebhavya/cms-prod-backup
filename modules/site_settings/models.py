from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.utils.translation import ugettext_lazy as _

@register_setting
class SocialMediaSettings(BaseSetting):
	'''only Facebook and Twitter'''
	class Meta:
		verbose_name = _('Social media settings')
		verbose_name_plural = _('Social media settings')

	facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
	twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")

	panels = [
		MultiFieldPanel([

			   FieldPanel("facebook"),
			   FieldPanel("twitter"),
			], heading="Social Media Settings")

	]





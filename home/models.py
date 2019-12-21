from django.db import models

from wagtail.core.models import Page
from wagtailvideos.models import Video 

class HomePage(Page):
	def get_context(self, request):
		context = super(HomePage, self).get_context(request)
		products = Video.objects.filter(scope="PUBLIC")
		context['product'] = products
		return context


class Comment(models.Model):
	video = models.ForeignKey(Video, related_name="comments", on_delete=62)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'Commented by {} on {}'.format(self.name, self.video)
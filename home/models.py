from django.db import models
from django.shortcuts import render
from wagtail.core.models import Page
from wagtailvideos.models import Video 
import pdb
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.http import HttpResponse, HttpResponseRedirect


class HomePage(RoutablePageMixin, Page):
	def get_videos(self):
		self.videos = Video.objects
		return self.videos

	def get_context(self, request):
		context = super(HomePage, self).get_context(request)
		context['product'] = self.get_videos().filter(scope=Video.PUBLIC)
		return context

	# def serve(self, request):
	# 	print(request.META.get('PATH_INFO'))
	# 	return render(request, self.template, self.get_context(request))

	
	@route(r'^search/$', name='search')
	def search_media(self, request, *args, **kwargs):
		self.videos = self.get_videos().filter(title__icontains=request.GET.get('search'))
		return render(request, 'home/search_results.html', {'videos': self.videos})


	@route(r'^watch/(?P<media_id>[-\w]+)/$', name='video_detail')
	def search_media(self, request, media_id,  *args, **kwargs):
		from .forms import CommentForm
		media = self.get_videos().get(id=media_id)
		comments = media.comments.filter(active=True)
		commentable = True
		category_videos = Video.objects.filter(channel=media.channel).exclude(id=media.id)

		if request.method == 'POST':
			form = CommentForm(request.POST)
			if form.is_valid():
				new_comment = form.save(commit=False)
				new_comment.video = media 
				new_comment.save()

				return HttpResponseRedirect('/watch/%s/'%media.id)
			print(form.errors)
			return render(request, 'home/video_detail.html', {'video': media, 'form': form, 'commentable': commentable, 'comments': comments, 'category_videos': category_videos})
		else:
			form = CommentForm()
		return render(request, 'home/video_detail.html', {'video': media, 'form': form, 'commentable': commentable, 'comments': comments, 'category_videos': category_videos})

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
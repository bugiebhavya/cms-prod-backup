from django.db import models
from django.db.models import Q
from django.shortcuts import render
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey 
from wagtailvideos.models import Video 
from modules.documents.models import CustomDocument as Document
import pdb
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel , MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.http import HttpResponse, HttpResponseRedirect
from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages

User = get_user_model()

class HomePageCarouselVideos(Orderable):
	'''Between 1 and 5 imagges for the home carousel '''
	page = ParentalKey("home.HomePage", related_name="carousel_media")
	carousel_video = models.ForeignKey(
		"wagtailvideos.Video",
		null = True, 
		blank = False,
		on_delete= models.SET_NULL,
		related_name = "+" 
		)
	

	carousel_document = models.ForeignKey(
		"documents.CustomDocument",
		null = True, 
		blank = True,
		on_delete= models.SET_NULL,
		related_name = "+" 
	)


	panels = [
		VideoChooserPanel("carousel_video"),
		DocumentChooserPanel("carousel_document")
	]

class HomePage(RoutablePageMixin, Page):
	content_panels = Page.content_panels + [
			
			MultiFieldPanel([

					InlinePanel("carousel_media", min_num=1, label="Media"),

				], heading="Carousel Media"),

	]
	
	# @route(r'^excel-watch/$')
	# def trending_media(self, request, *args, **kwargs):
	# 	return render(request, 'documents/excel.html', {})

class ReferenceUrlPage(RoutablePageMixin, Page):

	def get_videos(self):
		self.videos = Video.objects
		return self.videos

	def get_documents(self):
		self.documents = Document.objects
		return self.documents

	# def get_context(self, request):
	# 	context = super(HomePage, self).get_context(request)
	# 	return context

	# def serve(self, request):
	# 	print(request.META.get('PATH_INFO'))
	# 	return render(request, self.template, self.get_context(request))
	@route(r'^trending/$')
	def trending_media(self, request, *args, **kwargs):
		self.videos = self.get_videos().all()
		return render(request, 'dashboard/trending.html', {'videos': self.videos})
		
	@route(r'^search/$', name='search')
	def search_media(self, request, *args, **kwargs):
		self.videos = self.get_videos().filter(title__icontains=request.GET.get('q'))
		return render(request, 'home/search_results.html', {'videos': self.videos})


	@route(r'^watch/(?P<media_id>[-\w]+)/$', name='video_detail')
	def watch_media(self, request, media_id,  *args, **kwargs):
		from .forms import CommentForm
		print("-----------------------")
		media = self.get_videos().get(id=media_id)
		if media.scope == Video.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		comments = media.comments.all()
		commentable = True
		category_videos = Video.objects.filter(Q(tags__in=media.tags.all()) | Q(channel=media.channel)).exclude(id=media.id)
		
		return render(request, 'home/video_detail.html', {'video': media, 'commentable': commentable, 'comments': comments, 'category_videos': category_videos})

	@route(r'^doc-watch/(?P<media_id>[-\w]+)/$', name='document_detail')
	def document_detail(self, request, media_id,  *args, **kwargs):
		from .forms import CommentForm
		print("-----------------------")
		media = self.get_documents().get(id=media_id)
		if media.access == Document.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		media.update_views()
		comments = media.comments.all()
		commentable = True
		category_documents = Document.objects.filter(Q(tags__in=media.tags.all()) | Q(channel=media.channel)).exclude(id=media.id)
		
		return render(request, 'home/document_detail.html', {'base_url':settings.BASE_URL, 'document': media, 'commentable': commentable, 'comments': comments, 'category_documents': category_documents})

	# @route(r'^doc-render/$')
	# def document_viewer(self, request, *args, **kwargs):
	# 	return render(request, 'home/document_viewer.html',{})

class Comment(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = GenericForeignKey('content_type','object_id')
	user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, null=True)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'Commented by {} on {}'.format(self.user.username, self.content_object.title)
from django.db import models
from django.db.models import Q, Max, Sum, Count
from django.shortcuts import render
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey 
from wagtailvideos.models import Video 
from modules.documents.models import CustomDocument as Document
from modules.documents.models import CustomImage as Images

import pdb
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel , MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.http import HttpResponse, HttpResponseRedirect
from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from django.utils.timezone import localtime, make_aware, timedelta
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from datetime import datetime

User = get_user_model()

class HomePageCarouselVideos(Orderable):
	'''Between 1 and 5 imagges for the home carousel '''
	page = ParentalKey("home.HomePage", related_name="carousel_media")
	carousel_video = models.ForeignKey(
		"wagtailvideos.Video",
		null = True, 
		blank = False,
		on_delete= models.CASCADE,
		related_name = "+" 
		)
	

	carousel_document = models.ForeignKey(
		"documents.CustomDocument",
		null = True, 
		blank = True,
		on_delete= models.CASCADE,
		related_name = "+" 
	)

	carousel_image = models.ForeignKey(
		"documents.CustomImage",
		null = True, 
		blank = True,
		on_delete= models.CASCADE,
		related_name = "+" 
	)


	panels = [
		VideoChooserPanel("carousel_video"),
		DocumentChooserPanel("carousel_document"),
		ImageChooserPanel("carousel_image")
	]

class HomePage(RoutablePageMixin, Page):
	content_panels = Page.content_panels + [
			
			MultiFieldPanel([

					InlinePanel("carousel_media", min_num=1, label="Media"),

				], heading="Carousel Media"),

	]
	


class ReferenceUrlPage(RoutablePageMixin, Page):
	settings_panels = []
	def get_views(self, x):
            try:
                print(x.total_views)
                return x.total_views
            except:
                return 0

	def update_views(self, obj, user):
		if not user.is_anonymous:
			if not obj.media_views.filter(user=user).exists():
				from modules.dashboard.models import MediaView
				MediaView.objects.create(content_object=obj, user=user)

	def get_videos(self):
		self.videos = Video.objects
		return self.videos

	def get_documents(self):
		self.documents = Document.objects
		return self.documents

	def get_images(self):
		self.images = Images.objects
		return self.images

	# def get_context(self, request):
	# 	context = super(HomePage, self).get_context(request)
	# 	return context

	@route(r'^trending/$')
	def trending_media(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')

		videos = self.get_videos().annotate(views=Count("media_views__views")).order_by('-views')
		documents = self.get_documents().annotate(views=Count("media_views__views")).order_by('-views')
		images = self.get_images().annotate(views=Count("media_views__views")).order_by('-views')
		from itertools import chain
		media = list(chain(documents, videos, images))
		media_list = sorted(media, key=lambda x: self.get_views(x), reverse=True) 
		return render(request, 'dashboard/trending.html', {'medias': media_list})
		
	@route(r'^search/$', name='search')
	def search_media(self, request, *args, **kwargs):
		from django.db.models import Q
		videos = self.get_videos()
		documents = self.get_documents()
		images = self.get_images()
		media_list =[]
		has_result = False
		if request.GET.get('q', '') != '':
			videos = videos.filter(Q(title__istartswith=request.GET.get('q')) | Q(tags__name__istartswith=request.GET.get('q'))  )
			documents =documents.filter(Q(title__istartswith=request.GET.get('q')) | Q(tags__name__istartswith=request.GET.get('q')) )
			images = images.filter(Q(title__istartswith=request.GET.get('q')) | Q(tags__name__istartswith=request.GET.get('q')) )
			has_result = True
		if request.GET.get('publish_year', '') != '':
			try:
				videos = videos.filter(Q(publication_at__year=request.GET.get('publish_year')))
				documents =documents.filter(Q(publication_at__year=request.GET.get('publish_year')))
				images = images.filter(Q(publication_at__year=request.GET.get('publish_year')))
				has_result = True
			except Exception as ex:
				print(ex)

		if request.GET.get('publish_range', '') != '':
			try:
				publish_from = request.GET.get('publish_range').split(' - ')[0]
				publish_to = request.GET.get('publish_range').split(' - ')[1]
				date_publish_from = make_aware(datetime.strptime(publish_from, '%d/%m/%Y %I:%M %p'))
				date_publish_to = make_aware(datetime.strptime(publish_to, '%d/%m/%Y %I:%M %p'))

				videos = videos.filter(Q(publication_at__gte=date_publish_from)&Q(publication_at__lte=date_publish_to))
				documents =documents.filter(Q(publication_at__gte=date_publish_from)&Q(publication_at__lte=date_publish_to))
				images = images.filter(Q(publication_at__gte=date_publish_from)&Q(publication_at__lte=date_publish_to))
				has_result = True
			except Exception as ex:
				print(ex)

		from itertools import chain
		if has_result:
			media = list(chain(documents, videos, images))
			media_list = sorted(media, key=lambda x: self.get_views(x), reverse=True) 
		return render(request, 'home/search_results.html', {'medias': media_list})

	@route(r'^library/(?P<type>[-\w]+)/(?P<id>[-\w]+)/$', name="user_library")
	def user_library(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')

		from modules.documents.models import SubTopic, Topic, Subject, Area
		if kwargs.get('type') == 'subtopic':
			obj = SubTopic.objects.get(id=kwargs.get('id'))
			documents = obj.subtopic_documents.all()
		elif kwargs.get('type') == 'topic':
			obj = Topic.objects.get(id=kwargs.get('id'))
			documents = obj.topic_documents.all()

		elif kwargs.get('type') == 'subject':
			obj = Subject.objects.get(id=kwargs.get('id'))
			documents = obj.subject_documents.all()

		elif kwargs.get('type') == 'area':
			obj = Area.objects.get(id=kwargs.get('id'))
			documents = obj.area_documents.all()
		
		videos = obj.video_set.all()

		from itertools import chain
		media = list(chain(documents, videos))
		media_list = sorted(media, key=lambda x: self.get_views(x), reverse=True)

		return render(request, 'dashboard/library.html', {'medias': media_list, 'object': obj})


	@route(r'^watch/(?P<media_id>[-\w]+)/$', name='video_detail')
	def watch_media(self, request, media_id,  *args, **kwargs):
		from .forms import CommentForm
		media = self.get_videos().get(id=media_id)
		if media.scope == Video.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		self.update_views(media, request.user)
		comments = media.comments.all()
		commentable = True
		category_videos = Video.objects.filter(Q(tags__in=media.tags.all()) | Q(channel=media.channel)).exclude(id=media.id).distinct()
		
		return render(request, 'home/video_detail.html', {'video': media, 'commentable': commentable, 'comments': comments, 'category_videos': category_videos})

	@route(r'^doc-watch/(?P<media_id>[-\w]+)/$', name='document_detail')
	def document_detail(self, request, media_id,  *args, **kwargs):
		from .forms import CommentForm
		media = self.get_documents().get(id=media_id)
		if media.access == Document.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		self.update_views(media, request.user)
		comments = media.comments.all()
		commentable = True
		category_documents = Document.objects.filter(Q(tags__in=media.tags.all()) | Q(channel=media.channel)).exclude(id=media.id).distinct()
		
		return render(request, 'home/document_detail.html', {'base_url':settings.BASE_URL, 'document': media, 'commentable': commentable, 'comments': comments, 'category_documents': category_documents})


	@route(r'^view-image/(?P<media_id>[-\w]+)/$', name='image_detail')
	def image_detail(self, request, media_id,  *args, **kwargs):
		from .forms import CommentForm
		media = self.get_images().get(id=media_id)
		if media.access == Images.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		self.update_views(media, request.user)
		comments = media.comments.all()
		commentable = True
		category_documents = self.images.filter(Q(tags__in=media.tags.all()) | Q(channel=media.channel)).exclude(id=media.id).distinct()
		
		return render(request, 'home/document_detail.html', {'base_url':settings.BASE_URL, 'document': media, 'commentable': commentable, 'comments': comments, 'category_documents': category_documents})



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
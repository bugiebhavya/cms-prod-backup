from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from django.views.generic.detail import DetailView
from django.views import View
from django.conf import settings
from home.forms import CommentForm
from wagtailvideos.models import Video 
from modules.documents.models import CustomDocument as Document
from modules.documents.models import CustomImage as Images
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Area, Subject, Topic, SubTopic
from django.shortcuts import render
from modules.users.models import UserLog

class MediaDetailView(LoginRequiredMixin, DetailView):
	model = Document
	template_name = 'home/document_detail.html'

	def get_context_data(self, **kwargs):
		context = super(MediaDetailView, self).get_context_data(**kwargs)
		form = CommentForm()
		media = self.get_object()
		media.update_views()
		comments = media.comments.all()
		commentable = True
		category_documents = Document.objects.filter(Q(tags__in=media.tags.all()) | Q(channel=media.channel)).exclude(id=media.id)

		context.update({'base_url':settings.BASE_URL, 'document': media, 'form': form, 'commentable': commentable, 'comments': comments, 'category_documents': category_documents})

		return context

	def get(self, request, pk):
		media = Document.objects.get(id=pk)
		if media.access == Document.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		return super(MediaDetailView, self).get(request, id)


class WatchVideoView(View):
	def update_views(self, obj, user):
		if not user.is_anonymous:
			if not obj.media_views.filter(user=user).exists():
				from modules.dashboard.models import MediaView
				MediaView.objects.create(content_object=obj, user=user)

	def get(self, request, media_id):
		media = Video.objects.get(id=media_id)
		if media.scope == Video.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		self.update_views(media, request.user)
		comments = media.comments.all()
		commentable = True
		category_videos = Video.objects.filter(Q(tags__in=media.tags.all()) | Q(channel=media.channel)).exclude(id=media.id).distinct()
		
		if not request.user.is_anonymous:
			log = UserLog.objects.create(action='CONSULT MEDIA', username=request.user.username, media=media.title)
			log.save()

		return render(request, 'home/video_detail.html', {'video': media, 'commentable': commentable, 'comments': comments, 'category_videos': category_videos})

class ReadDocumentView(View):
	def update_views(self, obj, user):
		if not user.is_anonymous:
			if not obj.media_views.filter(user=user).exists():
				from modules.dashboard.models import MediaView
				MediaView.objects.create(content_object=obj, user=user)

	def get(self, request, media_id):
		media = Document.objects.get(id=media_id)
		if media.access == Document.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		self.update_views(media, request.user)
		comments = media.comments.all()
		commentable = True
		category_documents = Document.objects.filter(Q(tags__in=media.tags.all()) | Q(channel=media.channel)).exclude(id=media.id).distinct()

		if not request.user.is_anonymous:
			log = UserLog.objects.create(action='CONSULT MEDIA', username=request.user.username, media=media.title)
			log.save()

		return render(request, 'home/document_detail.html', {'base_url':settings.BASE_URL, 'document': media, 'commentable': commentable, 'comments': comments, 'category_documents': category_documents})

class ViewImageView(View):
	def update_views(self, obj, user):
		if not user.is_anonymous:
			if not obj.media_views.filter(user=user).exists():
				from modules.dashboard.models import MediaView
				MediaView.objects.create(content_object=obj, user=user)

	def get(self, request, media_id):
		media =Images.objects.get(id=media_id)
		if media.access == Images.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		self.update_views(media, request.user)
		comments = media.comments.all()
		commentable = True
		category_documents = Images.objects.filter(Q(tags__in=media.tags.all()) | Q(channel=media.channel)).exclude(id=media.id).distinct()

		if not request.user.is_anonymous:
			log = UserLog.objects.create(action='CONSULT MEDIA', username=request.user.username, media=media.title)
			log.save()
		
		return render(request, 'home/document_detail.html', {'base_url':settings.BASE_URL, 'document': media, 'commentable': commentable, 'comments': comments, 'category_documents': category_documents})



class FilterCatalogsView(SuperuserRequiredMixin, LoginRequiredMixin, APIView):
	def get(self, request, *args, **Kwargs):
		try:
			results = Area.objects.none()
			if request.GET.get('type') == 'area':
				results = Subject.objects.filter(area_id=request.GET.get('object'))

			elif request.GET.get('type') == 'subject':
				results = Topic.objects.filter(subject_id=request.GET.get('object'))

			elif request.GET.get('type') == 'topic':
				results = SubTopic.objects.filter(topic_id=request.GET.get('object'))

			return Response({'message': 'Result filteres', 'code': 200, 'data': results.values('id', 'name')})
		except Exception as ex:
			return Response({'code': 500, 'message': str(ex)})
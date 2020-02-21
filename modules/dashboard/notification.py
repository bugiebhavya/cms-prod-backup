from braces.views import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notifications
from django.utils.timezone import localtime, make_aware, timedelta
from rest_framework import serializers
from wagtailvideos.models import Video 
from modules.documents.models import CustomDocument as Document
from modules.documents.models import CustomImage as Images
import pdb
from django.urls import reverse_lazy

class VideoSerializer(serializers.ModelSerializer):
	thumbnail = serializers.SerializerMethodField(read_only=True)
	link_url = serializers.SerializerMethodField()
	class Meta:
		model = Video
		fields = ('id', 'title', 'thumbnail', 'link_url',)

	def get_thumbnail(self, obj):
		return obj.thumbnail.url

	def get_link_url(self, obj):
		return reverse_lazy('video_detail', kwargs={'media_id': obj.id})

class DocumentSerializer(serializers.ModelSerializer):
	thumbnail = serializers.SerializerMethodField(read_only=True)
	link_url = serializers.SerializerMethodField()
	class Meta:
		model = Document
		fields = ('id', 'title', 'thumbnail', 'link_url',)

	def get_thumbnail(self, obj):
		return obj.thumbnail.url

	def get_link_url(self, obj):
		return reverse_lazy('document_detail', kwargs={'media_id': obj.id})

class ImagesSerializers(serializers.ModelSerializer):
	thumbnail = serializers.SerializerMethodField(read_only=True)
	link_url = serializers.SerializerMethodField()
	class Meta:
		model = Images
		fields = ('id', 'title', 'thumbnail', 'link_url',)

	def get_thumbnail(self, obj):
		return obj.thumbnail.url

	def get_link_url(self, obj):
		return reverse_lazy('image_detail', kwargs={'media_id': obj.id})

class NotificationListSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d %B %Y %I:%M %p")
    
    class Meta:
        model = Notifications
        fields = ('id', 'content', 'content_type','created',)


    def get_content(self, obj):
        if isinstance(obj.content_object, Video):
            return VideoSerializer(obj.content_object).data

        elif isinstance(obj.content_object, Document):
            return DocumentSerializer(obj.content_object).data

        elif isinstance(obj.content_object, Images):
            return ImagesSerializers(obj.content_object).data
        return {}

    def get_content_type(self, obj):
    	return obj.content_type.name

class NotificationListView(LoginRequiredMixin, APIView):
	def get(self, request, *args, **Kwargs):
		notifications = Notifications.objects.filter(created__gte= localtime()-timedelta(days=7)).exclude(seen_users=request.user)
		notification_serializer = NotificationListSerializer(notifications, many=True)
		return Response({'code': 200, 'message':'Notification list fetched successfully', 'data': notification_serializer.data})

class RemoveNotificationView(LoginRequiredMixin, APIView):
	def get(self, request, pk):
		notification = Notifications.objects.get(pk=pk)
		notification.seen_users.add(request.user)
		notification.save()
		return Response({'code': 200, 'message':'Notification remove successfully'})
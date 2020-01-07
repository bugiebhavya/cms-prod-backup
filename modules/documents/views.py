from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from django.views.generic.detail import DetailView
from django.conf import settings
from home.forms import CommentForm
from modules.documents.models import CustomDocument as Document
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Area, Subject, Topic, SubTopic

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
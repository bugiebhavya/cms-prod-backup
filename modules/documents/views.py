from braces.views import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.conf import settings
from home.forms import CommentForm
from modules.documents.models import CustomDocument as Document
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q

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
		print("------------------------")
		media = Document.objects.get(id=pk)
		if media.access == Document.PRIVATE and request.user.is_anonymous:
			messages.warning(request, 'Please login to view this media.')
			return HttpResponseRedirect('/')
		return super(MediaDetailView, self).get(request, id)

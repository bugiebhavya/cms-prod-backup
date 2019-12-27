from django.db import models
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

class HomePageCarouselVideos(Orderable):
	'''Between 1 and 5 imagges for the home carousel '''
	page = ParentalKey("home.HomePage", related_name="carousel_videos")
	carousel_video = models.ForeignKey(
		"wagtailvideos.Video",
		null = True, 
		blank = False,
		on_delete= models.SET_NULL,
		related_name = "+" 
		)
	

	panels = [
			VideoChooserPanel("carousel_video")
	]

class HomePage(RoutablePageMixin, Page):
	content_panels = Page.content_panels + [
			
			MultiFieldPanel([

					InlinePanel("carousel_videos", min_num=1, label="Video"),

				], heading="Carousel Videos"),

	]
	def get_videos(self):
		self.videos = Video.objects
		return self.videos

	def get_documents(self):
		self.documents = Document.objects
		return self.documents

	# def get_context(self, request):
	# 	context = super(HomePage, self).get_context(request)
	# 	context['product'] = self.get_videos().filter(scope=Video.PUBLIC)
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
		media = self.get_videos().get(id=media_id)
		comments = media.comments.filter(active=True)
		commentable = True
		category_videos = Video.objects.filter(channel=media.channel).exclude(id=media.id)

		if request.method == 'POST':
			form = CommentForm(request.POST)
			if form.is_valid():
				new_comment = form.save(commit=False)
				new_comment.media = media 
				new_comment.save()

				return HttpResponseRedirect('/watch/%s/'%media.id)
			print(form.errors)
			return render(request, 'home/video_detail.html', {'video': media, 'form': form, 'commentable': commentable, 'comments': comments, 'category_videos': category_videos})
		else:
			form = CommentForm()
		return render(request, 'home/video_detail.html', {'video': media, 'form': form, 'commentable': commentable, 'comments': comments, 'category_videos': category_videos})

	@route(r'^doc-watch/(?P<media_id>[-\w]+)/$', name='document_detail')
	def document_detail(self, request, media_id,  *args, **kwargs):
		from .forms import CommentForm
		media = self.get_documents().get(id=media_id)
		comments = None#media.comments.filter(active=True)
		commentable = True
		category_documents = Document.objects.filter(tags__in=media.tags.all()).exclude(id=media.id)

		if request.method == 'POST':
		# 	form = CommentForm(request.POST)
		# 	if form.is_valid():
		# 		new_comment = form.save(commit=False)
		# 		new_comment.media = media 
		# 		new_comment.save()

		# 		return HttpResponseRedirect('/doc-watch/%s/'%media.id)
		# 	print(form.errors)
			return render(request, 'home/document_detail.html', {'document': media, 'form': form, 'commentable': commentable, 'comments': comments, 'category_documents': category_documents})
		else:
			form = CommentForm()
		return render(request, 'home/document_detail.html', {'document': media, 'form': form, 'commentable': commentable, 'comments': comments, 'category_documents': category_documents})


	@route(r'^doc-render/$')
	def document_viewer(self, request, *args, **kwargs):
		return render(request, 'home/document_viewer.html',{})


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
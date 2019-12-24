from django.views.generic import TemplateView 
from django.shortcuts import render, get_object_or_404
from wagtailvideos.models import Video 
from django.views.generic import View 
from .forms import AdminLoginForm, CommentForm
from django.contrib.auth.models import User
from django.shortcuts import render, reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.http import HttpResponse, HttpResponseRedirect 
from wagtailvideos.models import Video
from django.contrib.auth.mixins import LoginRequiredMixin
import pdb 
from django.views.generic import DetailView
from hitcount.views import HitCountDetailView
from django.db.models import F
# from modules.mostviews.models import MostView


def video_detail_view(request, videoid):
	video = get_object_or_404(Video, id=videoid)
	get_channel = video.channel
	category_videos = Video.objects.filter(channel=get_channel)
	count_hit = True

	# MostViewobjects.filter(pk=video.pk).update(count=F('count') + 1)

	comments = video.comments.filter(active=True)
	comment_submit = False 
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.video = video 
			new_comment.save()
			comment_submit = True
	else:
		form = CommentForm
	return render(request, 'home/video_detail.html', {'video': video, 'form': form, 'comment_submit': comment_submit, 'comments': comments, 'category_videos': category_videos})



class LoginView(View):
	def post(self, request):
		email = request.POST.get('email',None)
		password = request.POST.get('password',None)
		if email and password:
			if "@" in email:
				users = User.objects.filter(email__iexact=email)
			else:
				users = User.objects.filter(mobile_number__iexact=email)
			if users.exists() and users.first().check_password(password):
				user_obj = users.first()
				login(request, user_obj)
				messages.success(request, "Login Successfully")
				return HttpResponseRedirect('/')
			else:
				message = "Unable to login with given credentials"
				messages.info(request, message)
				return HttpResponseRedirect('/')
		else:
			message = "Invalid login details."
			messages.error(request, message)
			return HttpResponseRedirect('/')
from django.views.generic import TemplateView 
from django.shortcuts import render, get_object_or_404
from wagtailvideos.models import Video 
from django.views.generic import View 
from .forms import AdminLoginForm, CommentForm
from modules.users.models import User
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
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Comment
from modules.documents.models import CustomDocument as Document
# from modules.mostviews.models import MostView
from modules.documents.models import CustomImage as Images



class LoginView(View):
	def post(self, request):
		email = request.POST.get('email',None)
		password = request.POST.get('password',None)
		if email and password:
			if "@" in email:
				users = User.objects.filter(email__iexact=email)
			else:
				users = User.objects.filter(username__iexact=email)
			if users.exists() and users.first().check_password(password):
				user_obj = users.first()
				login(request, user_obj)
				messages.success(request, "Login Successfully")
				return HttpResponseRedirect('/users/dashboard')
			else:
				message = "Unable to login with given credentials"
				messages.info(request, message)
				return HttpResponseRedirect('/')
		else:
			message = "Invalid login details."
			messages.error(request, message)
			return HttpResponseRedirect('/')

class CommentView(LoginRequiredMixin,APIView):
	def post(self, request, *args, **Kwargs):
		user = request.user
		try:
			if request.data.get('content_type') == 'Video':
				media = Video.objects.get(id=request.data.get('object_id'))
			elif request.data.get('content_type') == 'Document':
				media = Document.objects.get(id=request.data.get('object_id'))
			else:
				media = Images.objects.get(id=request.data.get('object_id'))

			comment = Comment.objects.create(content_object=media, user=user, body=request.data.get('body'))
			return Response({'message': 'Your comment posted successfully', 'code': 200, 'data': {'username': user.username.title(), 'body': comment.body, 'created': comment.created.strftime('%b. %d, %Y, %I:%M %P.')}})
		except Exception as ex:
			return Response({'code': 500, 'message': str(ex)})
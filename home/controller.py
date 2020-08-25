from django.views.generic import TemplateView 
from django.shortcuts import render, get_object_or_404
from wagtailvideos.models import Video 
from django.views.generic import View 
from .forms import AdminLoginForm, CommentForm, UserCreationForm, UserEditForm
from modules.users.models import User, UserInterest, UserLog
from django.shortcuts import render, reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.http import HttpResponse, HttpResponseRedirect 
from wagtailvideos.models import Video
from django.contrib.auth.mixins import LoginRequiredMixin
import pdb 
from django.views.generic import DetailView
from hitcount.views import HitCountDetailView
from django.db.models import F, Q
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
			users = User.objects.filter(Q(email__iexact=email)|Q(username__iexact=email))
			if users.exists() and users.first().check_password(password):
				user_obj = users.first()
				login(request, user_obj)
				messages.success(request, "Login Successfully")
				log = UserLog.objects.create(action='LOGIN', username=user_obj.username)
				log.save()

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

from .models import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction
import pdb

class UserCreate(CreateView):
	model = User
	template_name = 'wagtailusers/users/create.html'
	form_class = UserCreationForm
	success_url = None

	def get_context_data(self, **kwargs):
		data = super(UserCreate, self).get_context_data(**kwargs)
		allInterest = UserInterest.objects.all()
		interestList = list(allInterest)
		listObjects = []
		if self.request.POST:
			data['form'] = UserCreationForm(self.request.POST)
			data['interestList'] = interestList
			
		else:
			data['interests'] = UserInterestFormSet()
			data['interestList'] = interestList
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		form.instance.created_by = self.request.user
		self.object = form.save(commit=False)
		if form.is_valid():
			user = form.save()
			listObj = []
			
			for i in range(1, len(context['interestList'])+1):
				print('percent: ',self.request.POST.get('percent-{}'.format(i)))
				listObj.append(UserInterestPercent(user = user, interest = UserInterest.objects.get(name=self.request.POST.get('interest-{}'.format(i))),percent = self.request.POST.get('percent-{}'.format(i))))
			UserInterestPercent.objects.bulk_create(listObj)
		else:
			data['interestList'] = interestList
		return super(UserCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('wagtailusers_users:index')

class UserUpdate(UpdateView):
	model = User
	template_name = 'wagtailusers/users/edit.html'
	form_class = UserEditForm
	success_url = None
	userId = None

	def get_context_data(self, **kwargs):
		data = super(UserUpdate, self).get_context_data(**kwargs)
		url = (self.request.build_absolute_uri(''))
		userId = url.split('/')[-2]
		allInterest = UserInterestPercent.objects.filter(user = User.objects.get(id = userId))
		interestList = list(allInterest)
		percentList = []
		for i in range(len(interestList)):
			percentList.append(interestList[i].percent)
		res = dict(zip(interestList, percentList))   
		if self.request.POST:
			data['form'] = UserEditForm(self.request.POST)
			data['interestList'] = interestList
			data['percentDict'] = self.request.POST.get('percentDict')
			print(self.request.POST.get('percentDict'))
			
		else:
			data['interestList'] = interestList
			data['percentDict'] = res
			print('hiii: ',data['percentDict'])
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		form.instance.created_by = self.request.user
		self.object = form.save(commit=False)
		print('heloooooo: ',context['interestList'],'      ',context['percentDict'])
		if form.is_valid():
			user = form.save()
			listObj = []
			print('hello: ',context['percentDict'])
			for i in range( len(context['interestList'])):
				UserInterestPercent.objects.filter(id = context['interestList'][i].id).update(percent = self.request.POST.get('percent-{}'.format(i+1)))
			# UserInterestPercent.objects.bulk_update(listObj, fields=['percent'])
		else:
			data['percentDict'] = context['percentDict']
			return data
		return super(UserUpdate, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('wagtailusers_users:index')
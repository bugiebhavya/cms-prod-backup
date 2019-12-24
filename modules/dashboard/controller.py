from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.shortcuts import render, reverse 
from django.contrib import messages
from wagtailvideos.models import Video 
from django.contrib import messages
from django.views.generic import View 
import pdb 
# Create your views here.


class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = "dashboard/index.html"
	def get(self, request, **kwargs):
		if not request.user:
			logout(request)
			messages.success(request, 'You are not allowed to access this page')
			return HttpResponseRedirect(reverse('/'))
		return super(DashboardView, self).get(request)

	def get_context_data(self, **kwargs):
		context = super(DashboardView, self).get_context_data(**kwargs)
		videos = Video.objects.all()
		context['videos'] = videos
		return context



class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Successfully logout, Please login.')
        return HttpResponseRedirect('/')


class TrendingView(LoginRequiredMixin, TemplateView): 
	template_name = "dashboard/trending.html"



class HistoryView(LoginRequiredMixin, TemplateView):
	template_name = 'dashboard/history.html'

# def searchMatch(query, item):
# 	if query in query in item.title.lower():
# 		return True
# 	return False

# def SearchView(request):
# 	query = request.GET.get('search')
# 	videotemp = Video.objects.all()
# 	videos = [item for item in videotemp if searchMatch(query, item)]
# 	if len(videos) == 0:
# 		message = "No Results found, Try Different KeyWord"
# 		messages.info(request, message)
# 	return render(request, 'search/search.html', {'videos': videos, 'messages': messages})



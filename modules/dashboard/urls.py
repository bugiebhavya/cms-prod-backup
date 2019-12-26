from django.urls import path, re_path, include
from .controller import *


urlpatterns = [
    
    path('logout', LogoutView.as_view(), name="user-logout"),
    ]
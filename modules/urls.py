from django.urls import path, re_path, include
from .dashboard import controller


urlpatterns = [
    path('dashboard', controller.DashboardView.as_view(), name='dashboard'),
    path('user-logout', controller.LogoutView.as_view(), name="user-logout"),
    path('trending', controller.TrendingView.as_view(), name="trending"), 
    path('history', controller.HistoryView.as_view(), name="history"), 

    ]




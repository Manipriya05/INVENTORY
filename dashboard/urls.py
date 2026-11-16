from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mall-overview/', views.mall_overview, name='mall_overview'),
    path('reports/', views.reports, name='reports'),
]
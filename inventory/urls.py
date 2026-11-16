from django.urls import path
from . import views
urlpatterns = [
    path('', views.stock_movement_list, name='stock_movement_list'),
    path('add/', views.add_stock_movement, name='add_stock_movement'),
]
from django.urls import path, include
from BlogManager import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('home/', views.HomeView.as_view(), name='home'),
    path('search/', views.HomeView.as_view(), name='search'),
]

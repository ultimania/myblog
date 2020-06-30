from django.urls import path, include
from myauth import views

urlpatterns = [
    path('', views.Login.as_view()),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
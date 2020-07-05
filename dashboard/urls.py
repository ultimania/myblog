from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/done', views.SignupDoneView.as_view(), name='signup_done'),
    path('signup/complete/<token>/', views.SignupCompleteView.as_view(), name='signup_complete'),
    path('list/', views.ListView.as_view(), name='list'),
    path('edit/', views.EditView.as_view(), name='edit'),
    path('update/<uuid:pk>', views.UpdateView.as_view(), name='update'),
    path('delete/<uuid:pk>', views.DeleteView.as_view(), name='delete'),
    path('result/', views.ResultView.as_view(), name='result'),
]

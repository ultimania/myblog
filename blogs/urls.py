from django.urls import path, include
from blogs import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('home/', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('list/', views.BlogBaseView.as_view(), name='list'),
    path('drafts/', views.DraftsView.as_view(), name='drafts'),
    path('post/', views.PostView.as_view(), name='post'),
    path('topic/<uuid:pk>', views.TopicView.as_view(), name='topic'),
    path('upload', views.UploadView.as_view(), name='upload'),
]

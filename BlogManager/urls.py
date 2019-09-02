from django.urls import path, include
from BlogManager import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('home/', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('list/', views.BlogBaseView.as_view(), name='list'),
    path('drafts/', views.DraftsView.as_view(), name='drafts'),
    path('post/', views.PostView.as_view(), name='post'),
    path('update/<uuid:pk>', views.TopicUpdateView.as_view(), name='update'),
    path('topic/<uuid:pk>', views.TopicDetailView.as_view(), name='topic'),
    path('preview/<uuid:pk>', views.TopicPreviewView.as_view(), name='preview'),
    path('upload', views.UploadView.as_view(), name='upload'),
]

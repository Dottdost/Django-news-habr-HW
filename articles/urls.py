from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('add/', views.add_article, name='add_article'),
    path('like/<int:pk>/', views.like_article, name='like_article'),
    path('dislike/<int:pk>/', views.dislike_article, name='dislike_article'),
]

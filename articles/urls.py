from django.urls import path
from . import views
from .views import  category_articles, categories_list

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/add/', views.add_article, name='add_article'),
    path('article/<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('article/<int:pk>/vote/<str:value>/', views.vote_article, name='vote_article'),
    path('article/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('popular/', views.popular_articles, name='popular_articles'),
    path('categories/', categories_list, name='categories'),
    path('categories/<slug:category>/', category_articles, name='category_articles'),
    path('favorites/', views.favorite_articles, name='favorites'),
    path('approve/<int:pk>/', views.approve_article, name='approve_article'),
    path('reject/<int:pk>/', views.reject_article, name='reject_article'),
    path('pending/', views.pending_articles, name='pending_articles'),
    path('panel/users/', views.users_list, name='users_list'),
    path('panel/users/<int:pk>/staff/', views.toggle_staff, name='toggle_staff'),
    path('panel/users/<int:pk>/active/', views.toggle_active, name='toggle_active'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newpost/', views.newPost, name='newpost'),
    path('<uuid:post_id>/', views.postDetail, name='post-details'),
    path('tag/<slug:tag_slug/', views.tags, name='tags'),
    path('<uuid:post_id>/like/', views.like, name='like'),
    path('<uuid:post_id>/favorite/', views.favorite, name='favorite')
]

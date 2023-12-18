from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('post/new/', views.create_post, name='create_post'),
    path('post/create/', views.create_post, name='post_create'),

]
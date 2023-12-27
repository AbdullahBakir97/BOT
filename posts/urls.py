from django.urls import path
from .views import create_post, generated_post

urlpatterns = [
    path('create/', create_post, name='create_post'),
     path('generated_post/', generated_post, name='generated_post'),
]
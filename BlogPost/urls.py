from django.urls import path
from . import views


urlpatterns = [
    path('blog/<int:pk>/', views.get_one_blog, name='get_one_blog'),
    path('all-blogs/', views.get_all_posts, name='all_blogs')
]

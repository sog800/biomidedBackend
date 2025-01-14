from django.urls import path
from . import views




urlpatterns = [
    path('blogs/<int:pk>/', views.get_one_blog, name='get_one_blog'),
    path('all-blogs/', views.get_all_posts, name='all_blogs'),
    path('like-blog/<int:pk>/', views.like_blog, name="like_blog"),
    path('<int:post_id>/comments/', views.get_comments, name='get_comments'),  # Fetch comments
    path('<int:post_id>/add-comment/', views.add_comment, name='add_comment'),  # Add a comment
]

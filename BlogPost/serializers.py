from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'description', 'blog_image', 'blog_video', 
                  'blog_likes', 'posted_at', 'comments']  # Include comments in the response

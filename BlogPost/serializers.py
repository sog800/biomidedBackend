from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username')
    author_bio = serializers.CharField(source='author.profile.bio', default='')
    author_image = serializers.ImageField(source='author.profile.profile_picture', default='')

    class Meta:
        model = BlogPost
        fields = ['id', 'author_name', 'title', 'description', 'content','blog_image', 'blog_video', 'author_image', 
                  'blog_likes', 'posted_at', 'comments', 'author_bio']  # Include comments in the response

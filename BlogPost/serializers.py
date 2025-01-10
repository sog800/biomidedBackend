from rest_framework import serializers
from .models import BlogPost, BlogComment

class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ['id', 'author', 'content', 'posted_at']

class BlogPostSerializer(serializers.ModelSerializer):
    comments = BlogCommentSerializer(many=True, read_only=True)  # Add the comments

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'description', 'content', 'blog_image', 'blog_video', 
                  'blog_likes', 'posted_at', 'comments']  # Include comments in the response

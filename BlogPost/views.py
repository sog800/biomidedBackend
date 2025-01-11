from django.shortcuts import render
from rest_framework import viewsets
from .models import BlogPost, BlogComment
from .serializers import BlogPostSerializer, BlogCommentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

# BlogPost ViewSet handling both CRUD and adding comments
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    # Custom action to add a comment to a blog post
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        blog_post = self.get_object()
        serializer = BlogCommentSerializer(data=request.data)

        if serializer.is_valid():
            # Save the comment with the blog post and associate it with the current user
            serializer.save(post=blog_post, author=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


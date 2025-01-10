from django.shortcuts import render
from rest_framework import viewsets
from .models import BlogPost
from .serializers import BlogPostSerializer
from .models import BlogPost, BlogComment
from .serializers import BlogPostSerializer, BlogCommentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

# clude for the blogpost
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


#coment
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        blog_post = self.get_object()
        serializer = BlogCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post=blog_post, author=request.user)  # Save comment with current user and blog post
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

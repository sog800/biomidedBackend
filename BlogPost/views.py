from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BlogPost
from .serializers   import  BlogPostSerializer
from django.db import DatabaseError
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



@api_view(['GET'])
def get_all_posts(request):
    try:
        all_blogs = BlogPost.objects.all()
        serializer = BlogPostSerializer(all_blogs, many=True)
        return Response(serializer.data)
    except DatabaseError:
        return Response({'content': 'Internal server error'}, status=500)
    


@api_view(['POST'])
def create_blog(request):
    serializer = BlogPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def delete_blog(request, pk):
    try:
        blog = BlogPost.objects.get(id=pk)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Blog not fount'}, status=status.HTTP_404_NOT_FOUND)
    blog.delete()
    return Response({'massege': 'blog deleted'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def edit_blog(request, pk):
    try:
        blog = BlogPost.objects.get(id=pk)
    except BlogPost.DoesNotExist:
        return Response({'error': 'blog not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BlogPostSerializer(blog, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({serializer.error, status.HTTP_400_BAD_REQUEST})

@api_view(['GET'])
def get_one_blog(request, pk):
    try:
        blog = BlogPost.objects.get(id = pk)
    except BlogPost.DoesNotExist:
        return Response({'error': 'blog doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = BlogPostSerializer(blog)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def like_blog(request, id):
    """
    View to handle likes on a BlogPost.
    Expects a JSON body: { "isLiked": true/false }
    """
    blog_post = get_object_or_404(BlogPost, id=id)
    data = request.data

    if 'isLiked' not in data:
        return Response({"error": "Missing 'isLiked' in request body."}, status=status.HTTP_400_BAD_REQUEST)

    is_liked = data['isLiked']
    if not is_liked:
        blog_post.blog_likes -= 1  # Unlike the post
    else:
        blog_post.blog_likes += 1  # Like the post

    blog_post.save()

    return Response({
        "id": blog_post.id,
        "likes": blog_post.blog_likes
    }, status=status.HTTP_200_OK)
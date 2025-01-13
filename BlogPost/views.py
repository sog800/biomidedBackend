from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import BlogPost
from .serializers   import  BlogPostSerializer
from django.db import DatabaseError
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from .models import BlogPost, BlogComment
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication




@api_view(['GET'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def get_one_blog(request, pk):
    try:
        blog = BlogPost.objects.get(id = pk)
    except BlogPost.DoesNotExist:
        return Response({'error': 'blog doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = BlogPostSerializer(blog)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([AllowAny])
def like_blog(request, pk):
    """
    View to handle likes on a BlogPost.
    Expects a JSON body: { "isLiked": true/false }
    """
    blog_post = get_object_or_404(BlogPost, id=pk)
    data = request.data

    if 'isLiked' not in data:
        return Response({"error": "Missing 'isLiked' in request body."}, status=status.HTTP_400_BAD_REQUEST)

    is_liked = data['isLiked']
    if is_liked:
        blog_post.blog_likes -= 1  # Unlike the post
    else:
        blog_post.blog_likes += 1  # Like the post

    blog_post.save()

    return Response({
        "id": blog_post.id,
        "likes": blog_post.blog_likes
    }, status=status.HTTP_200_OK)


# comment views



# View to fetch all comments for a blog post
@api_view(['GET'])
@permission_classes([AllowAny])
def get_comments(request, post_id):
    try:
        post = BlogPost.objects.get(id = post_id)
    except BlogPost.DoesNotExist:
        return Response({'error': 'blog post does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    comments = BlogComment.objects.filter(post=post).order_by('-posted_at')
    comments_data = [
        {
            'author': comment.author.username,
            'content': comment.content,
            'posted_at': comment.posted_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for comment in comments
    ]
    return JsonResponse(comments_data, safe=False)

# View to add a new comment
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])  # Use token-based authentication
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can comment
def add_comment(request, post_id):
    """
    Add a new comment to a blog post.
    """
    post = get_object_or_404(BlogPost, id=post_id)  # Get the blog post
    content = request.data.get('content')  # Get comment content from request data

    if not content:
        return Response({'message': 'Comment content cannot be empty'}, status=400)

    # Create and save the comment
    new_comment = BlogComment.objects.create(
        post=post,
        author=request.user,  # The authenticated user making the request
        content=content
    )

    return Response({
        'message': 'Comment added successfully',
        'comment': {
            'author': new_comment.author.username,
            'content': new_comment.content,
            'posted_at': new_comment.posted_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
    }, status=201)


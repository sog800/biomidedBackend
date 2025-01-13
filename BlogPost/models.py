from django.conf import settings  # Import settings to reference the custom user model
from django.db import models
from django.utils import timezone

# BlogPost model
class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')  # Use AUTH_USER_MODEL
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    blog_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    blog_video = models.FileField(upload_to='blog_videos/', null=True, blank=True)
    blog_likes = models.PositiveIntegerField(default=0)
    posted_at = models.DateTimeField(default=timezone.now)
    author_image = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    author_bio = models.TextField(default='')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted_at']  # Order by posted_at in descending order

# BlogComment model
class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    content = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

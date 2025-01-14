from django.contrib import admin
from .models import BlogPost, BlogComment



class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'posted_at')  # Display these fields in the list view
    list_filter = ('author',)  # Filter blog posts by author
    search_fields = ('title', 'content')  # Allow searching by title or content

admin.site.register(BlogPost, BlogPostAdmin)

admin.site.register(BlogComment)


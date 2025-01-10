from django.contrib import admin
from .models import BlogPost, BlogComment
from django.contrib.auth import get_user_model

# Register the User model (if using the default User model or a custom user model)
User = get_user_model()

class BlogCommentInline(admin.TabularInline):
    """
    Inline model for adding comments directly within the BlogPost model.
    This allows you to add/edit comments while editing a blog post.
    """
    model = BlogComment
    extra = 1  # Number of empty comment forms to display by default

class BlogPostAdmin(admin.ModelAdmin):
    """
    Customize the display of BlogPost model in the admin interface.
    """
    list_display = ('title', 'author', 'posted_at', 'blog_likes')
    search_fields = ('title', 'author__username', 'content')
    list_filter = ('posted_at', 'author')
    ordering = ('-posted_at',)
    
    # Add the inline BlogComment form to the BlogPost form
    inlines = [BlogCommentInline]

    # You can also customize how the fields are displayed or organized
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'content', 'author', 'blog_image', 'blog_video')
        }),
        ('Dates', {
            'fields': ('posted_at',)
        }),
    )

# Register the BlogPost model with the custom BlogPostAdmin
admin.site.register(BlogPost, BlogPostAdmin)

# Register the BlogComment model as well
class BlogCommentAdmin(admin.ModelAdmin):
    """
    Customize the display of BlogComment model in the admin interface.
    """
    list_display = ('author', 'post', 'posted_at', 'content')
    search_fields = ('author__username', 'content')
    list_filter = ('posted_at',)

# Register BlogComment with the admin interface
admin.site.register(BlogComment, BlogCommentAdmin)


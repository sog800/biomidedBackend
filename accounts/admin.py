from django.contrib import admin
from django.contrib.auth import get_user_model  # This gets your custom User model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Get the user model (either custom or default)
User = get_user_model()

# Customizing how users will appear in the admin panel
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)  # Order users by username

# Registering the customized User admin
admin.site.register(User, UserAdmin)

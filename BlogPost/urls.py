from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet

# Create a router and register the BlogPostViewSet
router = DefaultRouter()
router.register(r'blogposts', BlogPostViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include all the automatically generated routes for blogposts
]

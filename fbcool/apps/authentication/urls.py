from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet
app_name='seller'

router = routers.DefaultRouter()
router.register("post", PostViewSet, basename='postapi')

urlpatterns = [
    path('', include(router.urls)),
   
]
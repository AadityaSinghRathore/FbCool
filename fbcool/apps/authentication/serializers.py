from django.urls import path, include
from .models import Post
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'author', 'image','post_date','likes']
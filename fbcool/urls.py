"""fbcool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from authentication.views import PostListView,PostCreateView,SignUpView,PostUpdateView,PostDeleteView,CommentCreateView,PostDetail,LikeView ,validate_username,ProfileUpdateView
from django.conf.urls.static import static

from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SignUpView.as_view(), name='signup'),
   # path('home/', HomeView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('post/list/',PostListView.as_view(),name= "post-List"),
    path('post/detail/<int:pk>',PostDetail.as_view(),name= "post-Detail"),
    
    path('post/list/post/Create/',PostCreateView.as_view(),name= "post-Create"),

    path('profile/update/<int:pk>',ProfileUpdateView.as_view(),name= "profile-update"),

    path('post/delete/<int:pk>',PostDeleteView.as_view(),name= "post-delete"),
    path('post/update/<int:pk>',PostUpdateView.as_view(),name= "post-update"),
    path('comment/create/', CommentCreateView.as_view(),name= "post-comment"),
    #path('postlist/<int:pk>/addcomment/', CommentCreateView.as_view(), name='post-comment'),
   
   path('like/<int:pk>',LikeView,name='post-like'),
   path('ajax/validate_username', validate_username, name='validate_username'),

   path('oauth/', include('social_django.urls', namespace='social')), 
   path('accounts/', include('allauth.urls')),
   path('api-auth/', include('rest_framework.urls')),
   path('post_data/',include('authentication.urls', namespace='post'), ),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

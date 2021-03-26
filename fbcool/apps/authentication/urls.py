from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet,ExampleView,LoginView,RegisterView  
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenRefreshView
#   from auth.views import MyObtainTokenPairView, RegisterView  

app_name='seller'

router = routers.DefaultRouter()
router.register("post", PostViewSet, basename='postapi')

urlpatterns = [
    path('', include(router.urls)),
    path('example/', ExampleView.as_view(), name='example'),
    path('api-token-auth/', views.obtain_auth_token, name='api-tokn-auth'),
    path('login/',LoginView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   #path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
   ]
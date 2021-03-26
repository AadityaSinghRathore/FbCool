from django.urls import path, include
from .models import Post
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
 

# Serializers define the API representation.


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'author', 'image','post_date','likes']




class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={"input_type": "password"})
# # class LoginSerializer(serializers.Serializer):
    class Meta:  
        model = User       
        fields=['username','password'] 


#     def create(self, validated_data):
# #         return User.objects.create(**validated_data)
# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [ 'username','password']


class ShowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',  'username',  'auth_token' )




class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2' )
        

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match.","statuscode":201})
            
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
         
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user        
from django import forms
from .models import Post,Comment,User
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','author','image']

class CommentForm(forms.ModelForm):

    class Meta:
        model= Comment
        fields=['name','boady']        

class UserForm(forms.ModelForm):
    
    class Meta:
        model= User
        fields=['username','email']        
        
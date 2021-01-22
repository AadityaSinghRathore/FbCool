from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse
from datetime import datetime,date

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()      
    
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Image',upload_to='images')
    post_date=models.DateField(auto_now_add=True)
    

    def get_absolute_url(self):
        return reverse('home') 
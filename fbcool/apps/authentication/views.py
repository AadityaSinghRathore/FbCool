from django.shortcuts import render,redirect
from .forms import PostForm
# Create your views here.   
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView 
from . models import Post

class SignUpView(generic.CreateView):
   
    form_class = UserCreationForm
    
    template_name = 'signup.html'
    
    success_url = reverse_lazy('login')

class PostCreateView(CreateView):
   
    form_class = PostForm
    
    template_name='Post.html'
   
    success_url='home.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        
        #return render(request, "home.html")
       # return super(post-Create, self).form_valid(form)
        return redirect('/postlist/')

class PostListView(ListView):
    
    model= Post
    template_name = 'home.html'
    
    odering =['date_posted']        


from django.shortcuts import render,redirect
from .forms import PostForm,CommentForm
# Create your views here.   
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView  

from django.views.generic.edit import FormView 
from . models import Post,Comment
from django.views.generic.base import TemplateView
class SignUpView(generic.CreateView):
   
    form_class = UserCreationForm
    
    template_name = 'signup.html'
    
    success_url = reverse_lazy('home')
   
class HomeView(FormView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    success_url = '/postlist/' 


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

class CommentCreateView(CreateView):
    model=Comment

    form_class = CommentForm
    
    template_name='add_comment.html'

    def form_valid(self,form):
        form.instance.post_id=self.kwargs['pk']

        form.instance.name = self.request.user
        form.save()
        return super().form_valid(form)

    success_url='/postlist/'        

class PostListView(ListView):
    
    model= Post
    template_name = 'home.html'
    odering =['post_date']        

class PostUpdateView(UpdateView):
   
    model=Post
    form_class=PostForm
    template_name="postUpdate.html"
    success_url='/postlist/'
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        
        #return render(request, "home.html")
        # return super(post-Create, self).form_valid(form)
        return redirect('/postlist/')

class PostDeleteView(DeleteView):
    model=Post
    template_name="postDelete.html"
    
    success_url='/postlist/'        
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        
        #return render(request, "home.html")
        # return super(post-Create, self).form_valid(form)
        return redirect('/postlist/')   

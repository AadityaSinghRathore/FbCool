from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm,CommentForm
# Create your views here.   
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView  
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView 
from . models import Post,Comment
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string


def validate_username(request):
    
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def LikeView(request,pk):

    post=get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('post-Detail', args=[str(pk)]))


class SignUpView(generic.CreateView):
   
    form_class = UserCreationForm
    
    template_name = 'signup.html'

    
    success_url = reverse_lazy('login')
   
#class HomeView(FormView):
#    form_class = AuthenticationForm
#    template_name = 'registration/login.html'
 #   success_url = '/postlist/' 


# class PostCreateView(CreateView):
    
#     form_class = PostForm
    
#     model = Post
    
#     template_name='registration/newPost.html'
   
#     success_url='home.html'

    
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
        
#         #return render(request, "home.html")
#        # return super(post-Create, self).form_valid(form)
#         return redirect('/postlist/')
#     
    

class CommentCreateView(CreateView):
    model=Comment

    form_class = CommentForm
    
    template_name='add_comment.html'
    success_url='/postlist/'  
         

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['post_id'] = self.request.GET['post_id']
        return super().get_context_data(**kwargs)


    def form_valid(self,form):  

        extra_context={}
        form.instance.name = self.request.user
        data = form.save(commit=False)
        data.post_id = self.request.POST['post_id']
        data.user = self.request.user
        data.save()
 #    form.save()
#     return JsonResponse() 
        #return super().form_valid(form)
        extra_context['form_is_valid'] = True
        object_list = self.model.objects.all()
        extra_context['html_admin_user_list'] = render_to_string('include_post_list.html', {'post_list': object_list})
        return JsonResponse(extra_context)
    
      
       
    # def post(self, request, *args, **kwargs):
    #     import pdb; pdb.set_trace()
    #     extra_context = {}
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
            
    #         form.instance.user = self.request.user
    
    #         form.save()
    #         extra_context['form_is_valid'] = True
    #         object_list = self.model.objects.all()
    #         extra_context['html_admin_user_list'] = render_to_string('include_post_list.html', {'post_list': object_list})
    #     else:
    #         context = {'form' : form}
    #         extra_context['form_is_valid'] = False
    #         extra_context['html_form'] = render_to_string('add_comment.html', context )
    #     return JsonResponse(extra_context) 

class PostListView(ListView):
    
    model= Post
    template_name = 'home.html'
    odering =['post_date']  

class PostUpdateView(UpdateView):
   
    model=Post
    form_class=PostForm
    template_name="post_update.html"
    success_url='/postlist/'
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        
        #return render(request, "home.html")
        # return super(post-Create, self).form_valid(form)
        return redirect('/postlist/')

class PostDeleteView(DeleteView):
    model=Post
    template_name="post_delete.html"
    
    success_url='/postlist/'        
    
    def form_valid(self, form):

        form.instance.author = self.request.user
        form.save()
        
        #return render(request, "home.html")
        # return super(post-Create, self).form_valid(form)
        return redirect('/postlist/')   

class PostDetail(DetailView):
    model=Post
    template_name="post_detail.html"
    def get_context_data(self,*args,**kwargs):
         
        
         context = super(DetailView, self).get_context_data(**kwargs)
         

         stuff=get_object_or_404(Post,id=self.kwargs['pk']) 

         total_likes=stuff.total_likes()
         if stuff.likes.filter(id=self.request.user.id).exists():
            liked=True
            context['total_likes']=total_likes
            context['liked'] = liked   
         return  context  


class PostCreateView(CreateView):

    model = Post
    template_name = 'registration/new_post.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):

        extra_context = {}
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.save()
            extra_context['form_is_valid'] = True
            object_list = self.model.objects.all()
           
            extra_context['html_admin_user_list'] = render_to_string('include_post_list.html', {'post_list': object_list})
            
        else:
            context = {'form' : form}
            extra_context['form_is_valid'] = False
            extra_context['html_form'] = render_to_string('registration/new_post.html', context )
        return JsonResponse(extra_context)


# class CommentCreateView(CreateView):

#     model = Comment
#     template_name = "add_comment.html"
#     form_class = CommentForm
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = self.form_class()
#         return context

#     def post(self, request, *args, **kwargs):

#         extra_context = {}
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             post = get_object_or_404(Post, id=self.kwargs['pk'])
#             form.instance.user = self.request.user
#             form.instance.post = post
#             form.save()
#             extra_context['form_is_valid'] = True
#             object_list = self.model.objects.all()
#             extra_context['html_admin_user_list'] = render_to_string('include_post_list.html', {'post_list': object_list})
#         else:
#             context = {'form' : form}
#             extra_context['form_is_valid'] = False
#             extra_context['html_form'] = render_to_string('add_comment.html', context )
#         return JsonResponse(extra_context) 
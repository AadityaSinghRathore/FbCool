
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect,reverse,get_object_or_404
from .forms import PostForm,CommentForm
# Create your views here.   
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView  ,FormView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.template import RequestContext
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PostSerializer,LoginSerializer,ShowUserSerializer
from . models import Post,Comment
from rest_framework.permissions import IsAuthenticated , AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from . import utils
from .serializers import RegisterSerializer




class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request):
      
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message":'success', "status_code": status.HTTP_200_OK }, status=status.HTTP_200_OK)
        return Response({"message":serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST }, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  
    authentication_classes = [BasicAuthentication,TokenAuthentication]


class LoginView(generics.GenericAPIView):

    serializer_class= LoginSerializer
    queryset=User.objects.all()   
    permission_classes = [AllowAny] 
    


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            
            user = User.objects.get(username__iexact=serializer.validated_data['username'].lower())
        except:
            
            return Response(data={'detail' : 'user does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        password = serializer.validated_data['password']
        
        user = authenticate(username=user.username, password=password)
        if user is not None and (user.is_active == True ):
            if user.is_authenticated:
                utils.login_user(request, user)
                serializer = ShowUserSerializer(user)

                return Response(data=serializer.data, status=status.HTTP_200_OK )
            return Response(data={'detail': 'Unable to log in with provided credentials.'}, status=status.HTTP_401_UNAUTHORIZED)      
        return Response(data={'detail': 'Unable to log in with provided credentials.',"statusCode":200}, status=status.HTTP_401_UNAUTHORIZED)

        

class ExampleView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
           # None
             
            'message': 'Hello, World!', 
        }
        return Response(content)



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
    return HttpResponseRedirect(reverse('post-List', args=[str(pk)]))


class SignUpView(generic.CreateView):
   
    form_class = UserCreationForm
    
    template_name = 'signup.html'

    
    success_url = reverse_lazy('login')
   
     
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
            object_list = Post.objects.all()
           
            extra_context['html_admin_user_list'] = render_to_string('include_post_list.html', {'post_list': object_list})
            
        else:
            context = {'form' : form}
            extra_context['form_is_valid'] = False
            extra_context['html_form'] = render_to_string('registration/new_post.html', context )
        return JsonResponse(extra_context)
    

class CommentCreateView(CreateView):
    model=Comment

    form_class = CommentForm
    
    template_name='add_comment.html'
     
         
    
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
    
        extra_context['form_is_valid'] = True
        object_list = Post.objects.all()

        extra_context['html_admin_user_list'] = render_to_string('include_post_list.html', {'post_list': object_list} ) 
        return JsonResponse(extra_context)

    success_url='/post/list/'     


class PostListView(ListView):
    
    model= Post
    template_name = 'home.html'
    odering =['post_date'] 
  
class PostUpdateView(UpdateView):
   
    model=Post
    form_class=PostForm
    template_name="post_update.html"
    success_url='/post/list/'
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        
        #return render(request, "home.html")
        # return super(post-Create, self).form_valid(form)
        return redirect('/post/list/')

class PostDeleteView(DeleteView):
    model=Post
    template_name="post_delete.html"
    
    success_url='/post/list/'        
    
    def form_valid(self, form):

        form.instance.author = self.request.user
        form.save()
        
        #return render(request, "home.html")
        # return super(post-Create, self).form_valid(form)
        return redirect('/post/list/')   

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




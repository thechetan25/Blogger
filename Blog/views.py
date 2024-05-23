from typing import Any
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView,View
from django.views.generic import CreateView,ListView,DetailView
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeView,PasswordChangeDoneView
from .forms import signup,loginform,blogform,user_edit_form,user_detail_edit_form,change_password
from django.contrib.auth.models import User
from .models import blog,user_detail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils.functional import cached_property
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status



# Create your views here.

#------------------------------------------------------------------------------->
#Design Patterns
#-------------------------------------------------------------------------------->
#Create Blog Builder Design Pattern---------------------------------------------->
class CreateBlogViewBuilder:
    def __init__(self):
        self._template_name = None
        self._form_class = None
        self._model = None
        self._success_url = None
        self._login_required = True

    def set_template_name(self, template_name):
        self._template_name = template_name
        return self

    def set_form_class(self, form_class):
        self._form_class = form_class
        return self

    def set_model(self, model):
        self._model = model
        return self

    def set_success_url(self, success_url):
        self._success_url = success_url
        return self

    def set_login_required(self, login_required):
        self._login_required = login_required
        return self

    def build(self):
        class CustomCreateBlogView(LoginRequiredMixin, CreateView):
            template_name = self._template_name
            form_class = self._form_class
            model = self._model
            success_url = self._success_url

            def form_valid(self, form):
                form.instance.user = self.request.user
                return super().form_valid(form)

        if not self._login_required:
            CustomCreateBlogView.__bases__ = tuple(
                base for base in CustomCreateBlogView.__bases__ if base != LoginRequiredMixin
            )

        return CustomCreateBlogView

CreateBlogView = (
    CreateBlogViewBuilder()
    .set_template_name("blog/createblog.html")
    .set_form_class(blogform) 
    .set_model(blog)     
    .set_success_url("/blog/home")
    .set_login_required(False)
    .build()
)

#Login Singleton Design Pattern--------------------------------------------->

class SingletonLoggedUsers:
    _instance = None
    _logged_in_users = set()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def logged_in_users(self):
        return self._logged_in_users

class CustomLoginView(LoginView):
    form_class = loginform
    template_name = "blog/login.html"
    success_url = "/blog/home"

    def form_valid(self, form):
        singleton = SingletonLoggedUsers()
        username = form.cleaned_data.get('username')
        if username in singleton.logged_in_users:
            return self.render_to_response(self.get_context_data(form=form, error_message="User already logged in"))
        else:
            singleton.logged_in_users.add(username)
            return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = "/blog/login"

    def dispatch(self, request, *args, **kwargs):
        singleton = SingletonLoggedUsers()
        username = request.user.username
        if username in singleton.logged_in_users:
            singleton.logged_in_users.remove(username)
        return super().dispatch(request, *args, **kwargs)
    
    
#Iterator Design pattern for My_Blogs-------------------------------------------->
class BlogIterator:
    def __init__(self, user):
        self.user = user
        self.index = 0
        self.blogs = blog.objects.filter(user=user)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.blogs):
            blog = self.blogs[self.index]
            self.index += 1
            return blog
        else:
            raise StopIteration

class my_blogs(LoginRequiredMixin, ListView):
    template_name = "blog/myblogs.html"
    context_object_name = "object"

    def get_queryset(self):
        user = self.request.user
        return BlogIterator(user)
    
#Command Design Pattern----------------------------------------------------------->

class EditBlogCommand:
    def __init__(self, blog, data):
        self.blog = blog
        self.data = data

    def execute(self):
       
        self.blog.title = self.data['title']
        self.blog.content = self.data['content']
        self.blog.image = self.data.get('image')  
        self.blog.save()

class EditView(View):
    def get(self, request, slug):
        blog_instance = blog.objects.get(slug=slug)
        blog_form = blogform(instance=blog_instance)
        return render(request, "blog/edit.html", {"blog": blog_form, "data": blog_instance})

    def post(self, request, slug):
        blog_instance = blog.objects.get(slug=slug)
        blog_form = blogform(request.POST, request.FILES, instance=blog_instance)

        if blog_form.is_valid():
            
            edit_command = EditBlogCommand(blog_instance, request.POST)
           
            edit_command.execute()

        
            return redirect('my-blogs')

        return render(request, "blog/edit.html", {"blog": blog_form, "data": blog_instance})
    

#Password reset with Factory Design pattern-------------------------------------->

class PasswordViewFactory:
    @staticmethod
    def passreset_view():
        return PasswordResetView.as_view(
            template_name="blog/passreset.html",
            success_url="/blog/password-reset-done"
        )

    @staticmethod
    def pass_change():
        return PasswordChangeView.as_view(
            template_name="blog/change.html",
            form_class=change_password,
            success_url="/blog/password-change-done/"
        )

class PasswordViewTrigger(View):
    def post(self, request, *args, **kwargs):
        view_type = request.POST.get('view_type')
        if view_type == 'reset':
            return PasswordViewFactory.passreset_view()(request)
        elif view_type == 'change':
            return PasswordViewFactory.pass_change()(request)


#End of Design Patterns----------------------------------------------------------->
#--------------------------------------------------------------------------------->

class home(LoginRequiredMixin, ListView):
    template_name = "blog/home.html"
    model = blog
    context_object_name = "blogs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        
        if 'login-alert-shown' not in self.request.session:
            self.request.session['login-alert-shown'] = False

        if self.request.user.is_authenticated and not self.request.session['login-alert-shown']:
            messages.success(self.request, f"Logged in as {self.request.user.username}")
            self.request.session['login-alert-shown'] = True

        return context


class signupview(CreateView):
    form_class=signup
    model=User
    template_name="blog/signup.html"
    success_url="/blog/login"

class loginview(LoginView):
    form_class=loginform
    template_name="blog/login.html"
    success_url="/blog/home"
    

class create_blog(LoginRequiredMixin , CreateView):
    template_name="blog/createblog.html"
    form_class=blogform
    model=blog
    success_url="/blog/home"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# class my_blogs(LoginRequiredMixin , ListView):
#     template_name="blog/myblogs.html"
#     model=blog
#     context_object_name="object"

#     def get_queryset(self):
       
#         user = self.request.user
#         return blog.objects.filter(user = user)
    

class profile(View):
    def get(self ,request , str):

        user = User.objects.all().get(username = str)
        user_det =user_detail.objects.all().get(user = user)
        blogs = blog.objects.all().filter(user = user)
        auth_user = self.request.user
        liked = user.blog_likes.all()
        return render(request , "blog/profile.html" , {
            "object":user,
            "user_det":user_det,
            "blogs":blogs,
            "auth_user":auth_user,
            "liked":liked
        })


class blog_view(LoginRequiredMixin ,DetailView):
    template_name="blog/view.html"
    model = blog

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
    

class logout_view(LogoutView):
    next_page="/blog/login"
    
class forgot_view(PasswordResetView):
    template_name="blog/forgot.html"
    success_url="/blog/password-reset-done"

class passreset_view(PasswordResetView):
    template_name="blog/passreset.html"
    success_url="/blog/password-reset-done"
    

class passresetdone(PasswordResetDoneView):
    template_name="blog/passdone.html"
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
    
class passconfirm(PasswordResetConfirmView):
    template_name="blog/passconfirm.html"
    success_url="/blog/password-reset-complete"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uidb64"] = self.kwargs["uidb64"]
        context["token"] = self.kwargs["token"]
        return context

class passresetcomp(PasswordResetCompleteView):
    template_name="blog/passcomp.html"
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context   
    
        
class pass_change(PasswordChangeView):
    template_name="blog/change.html"
    form_class=change_password
    success_url="/blog/password-change-done/"
    
class change_done(PasswordChangeDoneView):
    template_name="blog/change_done.html"
    
    def get_extra_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        
        return context
        
        
class settings(View):
    def get(self, request):
        user = self.request.user
        det = user_detail.objects.get(user=user)
        
        user_edit = user_edit_form(instance=user)
        user_detail_edit = user_detail_edit_form(instance=det)
        

        visible_fields = user_detail_edit.visible_fields()
        half = len(visible_fields) // 2
        first_half = visible_fields[:half]
        second_half = visible_fields[half:]
        
        return render(request, "blog/settings.html", {
            "user": user_edit,
            "det": det,
            "User":user,
            "first_half_detail": first_half,
            "second_half_detail": second_half
        })
        
    def post(self, request):
        user = self.request.user
        det = user_detail.objects.get(user=user)
        
        user_edit = user_edit_form(request.POST, instance=user)
        user_detail_edit = user_detail_edit_form(request.POST, request.FILES, instance=det)
        
        visible_fields = user_detail_edit.visible_fields()
        half = len(visible_fields) // 2
        first_half = visible_fields[:half]
        second_half = visible_fields[half:]
        
        if user_edit.is_valid() and user_detail_edit.is_valid():
            user_edit.save()
            user_detail_edit.save()
            
            rpath = reverse("profile", args=[user.username])
            return HttpResponseRedirect(rpath)
        
        return render(request, "blog/settings.html", {
            "user": user_edit,
            "User":user,
            "det":det,
            "first_half_detail": first_half,
            "second_half_detail": second_half,
            "error":1
        })
        

class edit_view(View):
    def get(self  , request ,slug ):
        data = blog.objects.get(slug = slug)
        blogf = blogform(instance = data)
        return render(request , "blog/edit.html" , {
            "blog":blogf,
            "data":data
        })
    
    def post(self , request , slug):
        data = blog.objects.get(slug = slug)
        blogf = blogform(request.POST ,request.FILES ,instance = data)

        if blogf.is_valid():
            blogf.save()

            rpath = reverse('my-blogs')
            return redirect(rpath)
        
        return render(request , "blog/edit.html" , {
            "blog":blogf,
            "data":data
        })

        
class delete_view(View):
    def get(self  , request ,slug ):
        data = blog.objects.get(slug = slug)
        data.delete()

        rpath = reverse("my-blogs")
        
        return redirect(rpath)
    
class like_view(View):
    def post(self,request,id):
        user = self.request.user
        blog.objects.get(id = id).likes.add(user)

        slug = blog.objects.get(id =id).slug

        rpath = reverse("blog-view" , args=[slug])

        return redirect(rpath)
    
class rlike_view(View):
    def post(self,request,id):
        user = self.request.user
        blog.objects.get(id = id).likes.remove(user)

        slug = blog.objects.get(id =id).slug

        rpath = reverse("blog-view" , args=[slug])

        return redirect(rpath)

        

            
            
        
        
        
        
        
        



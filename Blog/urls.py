from django.urls import path
from .import views



urlpatterns = [
    path("home" ,views.home.as_view() , name="home"),
    path("signup" , views.signupview.as_view() , name ="signup"),
    path("login" , views.CustomLoginView.as_view() , name="login"),
    path("create-blog" , views.CreateBlogView.as_view() , name="create-blog"),
    path("my-blogs" , views.my_blogs.as_view() , name="my-blogs"),
    path("view/<slug:slug>" , views.blog_view.as_view() , name="blog-view"),
    path("users/<str:str>" , views.profile.as_view() , name="profile"),
    path("logout" , views.CustomLogoutView.as_view() , name="logout"),
    path("password-reset" , views.passreset_view.as_view() , name="reset"),
    path("password-reset-done" , views.passresetdone.as_view() , name="resetdone"),
    path("pas-reset/<uidb64>/<token>" , views.passconfirm.as_view() , name="password_reset_confirm"),
    path("pass-reset-complete" , views.passresetcomp.as_view() , name="reset_complete"),
    path("edit/<slug:slug>" , views.EditView.as_view() , name="edit"),
    path("delete/<slug:slug>" , views.delete_view.as_view() , name="delete"),
    path("like/<int:id>" , views.like_view.as_view() , name="like"),
    path("rlike/<int:id>", views.rlike_view.as_view() , name="rlike"),
    path("settings" , views.settings.as_view() , name="settings"),
    path("password-change" , views.pass_change.as_view() , name="password-change"),
    path("password-change-done" , views.change_done.as_view() , name="password-change-done"),
    path("forgot", views.forgot_view.as_view() , name="forgot"),
    path("password_reset" , views.PasswordViewTrigger.as_view() , name="passet")
]

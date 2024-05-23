from typing import Any
from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import user_detail,blog
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget

class signup(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name","last_name","email","username"
        ]
        labels={
            "first_name":"Enter Your First name",
            "last_name":"Enter Your Last name",
            "email":"Enter Your Email",
            "username":"Enter username"
        }

        help_texts={
             "first_name":"",
            "last_name":"",
            "email":"",
            "username":""
        }

        widgets={
            "first_name":forms.TextInput(attrs={'class':"form-control" ,'placeholder':"First Name"}),
            "last_name":forms.TextInput(attrs={'class':"form-control" ,'placeholder':"Last Name"}),
            "username":forms.TextInput(attrs={'class':"form-control" ,'placeholder':" Username"}),
            "email":forms.EmailInput(attrs={'class':"form-control" ,'placeholder':"Email Id"}),
        }

    date_of_birth =forms.DateField(required=True , label="Enter your date of birth" , widget=forms.DateInput(attrs={'class':"form-control" ,'placeholder':"DOB (YYYY-MM-DD)" ,'type':'date'}))
    phone_number =forms.CharField(required=True , label="Enter your Mobile number" , widget=forms.TextInput(attrs={'class':"form-control" ,'placeholder':"Phone Number"}))

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label="Enter Your password"
        self.fields["password2"].label="Renter Your password"
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""
        self.fields['first_name'].widget.attrs["autocomplete"] = "off"
        self.fields['password1'].widget.attrs["autocomplete"] = "off"
        self.fields['password1'].widget.attrs["class"] = "form-control"
        self.fields['password1'].widget.attrs["placeholder"] = "Password"
        self.fields['password2'].widget.attrs["autocomplete"] = "off"
        self.fields['password2'].widget.attrs["class"] = "form-control"
        self.fields['password2'].widget.attrs["placeholder"] = "Re-enter Password"
        self.fields['last_name'].widget.attrs["autocomplete"] = "off"
        self.fields['username'].widget.attrs["autocomplete"] = "off"
        self.fields['email'].widget.attrs["autocomplete"] = "off"

    def save(self , commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        date_of_birth = self.cleaned_data['date_of_birth']
        phone_number = self.cleaned_data['phone_number']

        user_detail.objects.create(dob=date_of_birth, phn=phone_number, user=user)

        return user


class loginform(AuthenticationForm):
    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].label="Enter Your Username"
        self.fields["password"].label="Enter Your password"
        self.fields['password'].widget.attrs["class"] = "form-control"
        self.fields['password'].widget.attrs["placeholder"] = "Password"
        self.fields['username'].widget.attrs["class"] = "form-control"
        self.fields['username'].widget.attrs["placeholder"] = "Username"



class blogform(forms.ModelForm):
    class Meta:
        model = blog
        fields = ["title", "content", "cover"]
        labels = {
            "title": "Title",
            "content": "Content",
            "cover": "Cover Pic"
        }
        widgets = {
            'content': CKEditorWidget(attrs={'id': 'content'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of your post'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        
class user_edit_form(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(user_edit_form, self).__init__(*args, **kwargs)
        
        icon_classes = {
            "first_name":"bi bi-pen-fill",
            "last_name":"bi bi-pen-fill",
            "username":"Ybi bi-person-fill",
            "email":"bi bi-envelope-fill"
        }
        
        for field_name, icon_class in icon_classes.items():
            if field_name in self.fields:
                icon_html = f'<i class="{icon_class}"></i>'
                label_with_icon = mark_safe(f'{icon_html} {self.fields[field_name].label}')
                self.fields[field_name].label = label_with_icon
                
    class Meta:
        model = User
        fields = [
           "username", "first_name","last_name","email",
        ]
        labels={
            "first_name":"Your First Name",
            "last_name":"Your Last name",
            "username":"Your Username",
            "email":"Your Email"
        }
        widgets={
            "first_name":forms.TextInput(attrs={'class':"form-control" ,'placeholder':"First Name"}),
            "last_name":forms.TextInput(attrs={'class':"form-control" ,'placeholder':"Last Name"}),
            "username":forms.TextInput(attrs={'class':"form-control" ,'placeholder':" Username"}),
            "email":forms.EmailInput(attrs={'class':"form-control" ,'placeholder':"Email Id"}),
        }
        
class user_detail_edit_form(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(user_detail_edit_form, self).__init__(*args, **kwargs)
        
        icon_classes = {
            "dob":"bi bi-calendar-range-fill",
            "phn":"bi bi-telephone",
            "c_img":"bi bi-image",
            "p_img":"bi bi-file-image",
            "insta_link": "bi bi-instagram",
            "twitter_link": "bi bi-twitter",
            "linked_link": "bi bi-linkedin",
            "facebook_link": "bi bi-facebook",
        }
        
        for field_name, icon_class in icon_classes.items():
            if field_name in self.fields:
                icon_html = f'<i class="{icon_class}"></i>'
                label_with_icon = mark_safe(f'{icon_html} {self.fields[field_name].label}')
                self.fields[field_name].label = label_with_icon
                
    class Meta:
        model = user_detail
        fields =["dob","phn","c_img","p_img","insta_link","linked_link","twitter_link","facebook_link"]
        widgets={
            "dob":forms.DateInput(attrs={'class':"form-control" ,'placeholder':"Date of Birth" , "type":"date"}),
            "phn":forms.TextInput(attrs={'class':"form-control" ,'placeholder':"Last Name"}),
            "c_img":forms.ClearableFileInput(attrs={'class':"form-control" ,'placeholder':" CoverImage "}),
            "p_img":forms.ClearableFileInput(attrs={'class':"form-control" ,'placeholder':"Profile Image"}),
            "insta_link":forms.URLInput(attrs={'class':"form-control" ,'placeholder':"Instagram"}),
            "twitter_link":forms.URLInput(attrs={'class':"form-control" ,'placeholder':"Twitter"}),
            "linked_link":forms.URLInput(attrs={'class':"form-control" ,'placeholder':"Linked In"}),
            "facebook_link":forms.URLInput(attrs={'class':"form-control" ,'placeholder':"Facebook"})
        }
        labels={
            "dob":"Date of Birth",
            "phn":"Mobile Number",
            "c_img":"Cover Image",
            "p_img":"Profile Image",
            "insta_link":"Instagram Link",
            "twitter_link":"Twitter Link",
            "linked_link":"Linked In Link",
            "facebook_link":"Facebook Link"
        }
            
            
class change_password(PasswordChangeForm):
    def __init__(self, user: AbstractBaseUser | None, *args: Any, **kwargs: Any):
        super().__init__(user, *args, **kwargs)
        self.fields["old_password"].label="Enter Your Old Password"
        self.fields["new_password1"].label="Enter Your  New Password"
        self.fields["new_password2"].label="re-enter Your New Password"
        self.fields['new_password1'].widget.attrs["class"] = "form-control"
        self.fields['new_password1'].widget.attrs["placeholder"] = "New Password"
        self.fields['new_password2'].widget.attrs["class"] = "form-control"
        self.fields['new_password2'].widget.attrs["placeholder"] = "Reenter Password"
        self.fields['old_password'].widget.attrs["class"] = "form-control"
        self.fields['old_password'].widget.attrs["placeholder"] = "Old Password"

        
    




    







    
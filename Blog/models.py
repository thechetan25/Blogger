from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.timezone import timezone
from django.utils.timezone import now as tz_now
from datetime import timedelta
from django.utils.dateformat import DateFormat
import re

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now as tz_now
from django.utils.dateformat import DateFormat

class user_detail(models.Model):
    dob = models.DateField(blank=False, null=False)
    phn = models.CharField(default="", max_length=15, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE ,related_name="user_det")
    p_img = models.ImageField(upload_to="profile_images", blank=True, null=True)
    c_img = models.ImageField(upload_to="cov_prof_images", blank=True, null=True)
    since = models.DateField(default='2024-02-25' ,blank=True, null=True)
    insta_link =models.URLField(blank=True,null=True , max_length=255)
    linked_link =models.URLField(blank=True,null=True , max_length=255)
    twitter_link = models.URLField(blank=True, null=True, max_length=255)
    facebook_link = models.URLField(blank=True, null=True, max_length=255)
    verified =models.BooleanField(default=False,blank=True, null=True)

    def save(self, *args, **kwargs):
        current_date = tz_now()
        self.since = current_date.replace(day=1)
        return super().save(*args, **kwargs)
    
    @property
    def display_since(self):
        if self.since:
            return DateFormat(self.since).format('F Y') 
        else:
            return "No date available"
        
    @property
    def extract_username(self):
        if self.insta_link:
            regex = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/([a-zA-Z0-9_\.]+)\/?"
            match = re.match(regex, self.insta_link)
            if match:
                return match.group(1)
            else:
                return None
        else:
            return None
        
    @property
    def extract_linked_username(self):
        if self.linked_link:
            regex = r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/([a-zA-Z0-9_\-]+)\/?"
            match = re.match(regex, self.linked_link)
            if match:
                return match.group(1)
            else:
                return None
        else:
            return None
        
    @property
    def extract_twitter_username(self):
        if self.twitter_link:
            regex = r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/([a-zA-Z0-9_]+)\/?"
            match = re.match(regex, self.twitter_link)
            if match:
                return match.group(1)
            else:
                return None
        else:
            return None
        
    @property
    def extract_facebook_username(self):
        if self.facebook_link:
            regex = r"(?:https?:\/\/)?(?:www\.)?facebook\.com\/([a-zA-Z0-9_\.]+)\/?"
            match = re.match(regex, self.facebook_link)
            if match:
                return match.group(1)
            else:
                return None
        else:
            return None
        
    def __str__(self):
        return f"{self.user.username}"

    

class blog(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    content = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="blogs")
    slug = models.SlugField(blank=True, null=False)
    likes = models.ManyToManyField(User, related_name="blog_likes")
    cover = models.ImageField(upload_to="cover_images", blank=True, null=True)
    posted = models.DateTimeField(default = tz_now , blank =True, null=True)
    updt = models.DateTimeField(default=tz_now, blank=True, null=True)

    
    @property
    def last_update_display(self):
        ist_time = self.updt.astimezone(timezone(timedelta(hours=5, minutes=30))) 
        now = tz_now()
        time_elapsed = now - ist_time
        if time_elapsed.total_seconds() < 60:
            return f"{int(time_elapsed.total_seconds() // 1)} seconds ago"
        elif time_elapsed.total_seconds() < 60 * 60:
            return f"{int(time_elapsed.total_seconds() // 60)} minutes ago"
        elif time_elapsed.total_seconds() < 24 * 60 * 60:
            return f"{int(time_elapsed.total_seconds() // 3600)} hours ago"
        else:
            return f"on {ist_time.strftime('%B %d, %Y')}"
        
    @property
    def posted_date_display(self):
        ist_time = self.posted.astimezone(timezone(timedelta(hours=5, minutes=30))) 
        return ist_time.strftime('%B %d, %Y') 



    def __str__(self):
        return f"{self.title} {self.user}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.updt = tz_now() 
        return super().save(*args, **kwargs)


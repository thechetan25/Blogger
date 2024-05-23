from django.contrib import admin
from .models import blog,user_detail

# Register your models here.

class blogadmin(admin.ModelAdmin):
   prepopulated_fields = {'slug': ('title',)}

admin.site.register(blog ,blogadmin)
admin.site.register(user_detail)

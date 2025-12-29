from django.contrib import admin
from django.contrib.auth.models import Group
from home.model import Profile , PostModel

# Register your models here.

admin.site.register(Profile)
admin.site.register(PostModel)
user_group,creatd = Group.objects.get_or_create(name = 'user')

admin_group, created = Group.objects.get_or_create(name = 'admin')

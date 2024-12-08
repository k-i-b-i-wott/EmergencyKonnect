from django.contrib import admin

# Register your models here.

from .models import  UserRequest
from .models import User




admin.site.register(UserRequest)

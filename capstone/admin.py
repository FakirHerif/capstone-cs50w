from django.contrib import admin
from .models import User,Category,Input

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Input)
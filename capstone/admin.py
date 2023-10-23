from django.contrib import admin
from .models import User,Category,Input,Comment,Site
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups',  'inputBookmark')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


class InputAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isActive', 'owner', 'category', 'content')
    list_filter = ('isActive', 'category', 'owner')
    search_fields = ('title', 'content', 'owner__username', 'category__categoryName')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'categoryImage')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'input', 'category', 'message')
    list_filter = ('category', 'author', 'input')
    search_fields = ('author__username', 'input__title', 'category__categoryName', 'message')

class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'url', 'input', 'category')
    list_filter = ('category', 'name', 'input', 'author')
    search_fields = ('author__username', 'input__title', 'category__categoryName', 'name', 'url')
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Input, InputAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Site, SiteAdmin)
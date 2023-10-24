from django.contrib import admin
from .models import User,Category,Input,Comment,Site, Note
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups',  'inputBookmark')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


class InputAdmin(admin.ModelAdmin):
    list_display = ('id', 'isActive', 'owner', 'category', 'title', 'content')
    list_filter = ('isActive', 'category', 'owner')
    search_fields = ('title', 'content', 'owner__username', 'category__categoryName')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'categoryImage')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'category', 'input', 'message')
    list_filter = ('category', 'author', 'input')
    search_fields = ('author__username', 'input__title', 'category__categoryName', 'message')

class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'category', 'input', 'name', 'url')
    list_filter = ('category', 'name', 'input', 'author')
    search_fields = ('author__username', 'input__title', 'category__categoryName', 'name', 'url')

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'category', 'input', 'title', 'content')
    list_filter = ('category', 'title', 'input', 'owner')
    search_fields = ('owner__username', 'input__title', 'category__categoryName', 'title', 'content')
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Input, InputAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Note, NoteAdmin)
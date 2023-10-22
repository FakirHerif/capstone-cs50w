from django.contrib import admin
from .models import User,Category,Input,Comment,Site

# Register your models here.


class InputAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isActive', 'owner', 'category', 'content')
    list_filter = ('isActive', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'categoryImage')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'input', 'category', 'message')

class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'url')

admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Input, InputAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Site, SiteAdmin)
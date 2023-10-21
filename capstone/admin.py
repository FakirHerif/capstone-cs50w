from django.contrib import admin
from .models import User,Category,Input,Comment

# Register your models here.


class InputAdmin(admin.ModelAdmin):
    list_display = ('title', 'isActive', 'owner', 'category')
    list_filter = ('isActive', 'category')


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Input, InputAdmin)
admin.site.register(Comment)
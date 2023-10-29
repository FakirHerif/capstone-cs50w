from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=60)
    categoryImage = models.ImageField(upload_to='category_images', blank=True, null=True)

    def __str__(self):
        return self.categoryName

class Input(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=6000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    isActive = models.BooleanField(default=True)
    bookmark = models.ManyToManyField(User, blank=True, null=True, related_name="inputBookmark")

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    input = models.ForeignKey(Input, on_delete=models.CASCADE, blank=True, null=True, related_name="inputComment")
    message = models.CharField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="categoryComment")
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} comment on {self.input}"
    

class Site(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userSite")
    input = models.ForeignKey(Input, on_delete=models.CASCADE, blank=True, null=True, related_name="inputSite")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="categorySite")
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=60)

    def __str__(self):
        return self.name
    
class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null=True, related_name="userNote")
    input = models.ForeignKey(Input, on_delete=models.CASCADE, blank=True, null=True, related_name="inputNote")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="categoryNote")
    title = models.CharField(max_length=60)
    content = models.CharField(max_length=3600)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
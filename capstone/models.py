from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=60)

    def __str__(self):
        return self.categoryName

class Input(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=6000)
    url = models.CharField(max_length=60)
    sites = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title
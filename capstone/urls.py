from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createInput, name="create"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("input/<int:id>", views.input, name="input"),
    path("removeBookmark/<int:id>", views.removeBookmark, name="removeBookmark"),
    path("addBookmark/<int:id>", views.addBookmark, name="addBookmark")
]

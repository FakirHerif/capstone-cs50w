from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createInput, name="create"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path('input/<int:id>/<slug:slug>/', views.input, name='input'),
    path('removeBookmark/<int:id>/<slug:slug>/', views.removeBookmark, name='removeBookmark'),
    path('addBookmark/<int:id>/<slug:slug>/', views.addBookmark, name='addBookmark'),
    path("bookmark", views.displayBookmark, name="bookmark"),
    path("addComment/<int:id>/<slug:slug>/", views.addComment, name="addComment"),
    path('search/', views.search, name='search'),
    path('add_site/<int:id>/<slug:slug>/', views.addSite, name='add_site'),
    path('add_note/<int:id>/<slug:slug>/', views.addNote, name='add_note')
]

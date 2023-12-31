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
    path('add_note/<int:id>/<slug:slug>/', views.addNote, name='add_note'),
    path('get_sites/<int:id>/', views.get_sites, name='get_sites'),
    path('get_notes/<int:id>/', views.get_notes, name='get_notes'),
    path('get_comments/<int:id>/', views.get_comments, name='get_comments'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('edit_comment/<int:id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import User, Category, Input, Comment, Site, Note


def index(request):
    activeInput = Input.objects.filter(isActive = True)
    allCategories = Category.objects.all()
    return render(request, "capstone/index.html", {
        "input": activeInput,
        "categories": allCategories
    })

def search(request):
    categories = Category.objects.all()
    query = request.GET.get('query')
    if query:
        results = Input.objects.filter(title__icontains=query)
    else:
        results = Input.objects.none()
    return render(request, 'capstone/search_results.html', {'results': results, 'query': query, "categories": categories })


def input(request, id, slug):
    inputData = Input.objects.get(pk=id)
    categories = Category.objects.all()
    isInputInBookmark = request.user in inputData.bookmark.all()
    allComments = Comment.objects.filter(input=inputData).order_by('-date_posted')
    allNotes = Note.objects.filter(input=inputData)
    return render(request, "capstone/input.html", {
        "input": inputData,
        "isInputInBookmark": isInputInBookmark,
        "allComments": allComments,
        "allNotes": allNotes,
        "categories": categories
    })


def addSite(request, id, slug):
    if request.method == "POST":
        site_name = request.POST.get("site_name")
        site_url = request.POST.get("site_url")
        input_data = get_object_or_404(Input, pk=id)
        user = request.user
        category = input_data.category
        new_site = Site(name=site_name, url=site_url, input=input_data, author=user, category=category)
        
        new_site.save()
    return HttpResponseRedirect(reverse("input", args=(id, slug)))


def get_sites(request, id):
    input_data = get_object_or_404(Input, pk=id)
    sites = Site.objects.filter(input=input_data)
    data = {
        "sites": [{"name": site.name, "url": site.url} for site in sites]
    }
    return JsonResponse(data)

def get_notes(request, id):
    input_data = get_object_or_404(Input, pk=id)
    notes = Note.objects.filter(input=input_data)
    data = {
        "notes": [{"title": note.title, "content": note.content, "id": note.id,  "owner": note.owner.username, "date_posted": note.date_posted} for note in notes]
    }
    return JsonResponse(data)


def get_comments(request, id):
    input_data = get_object_or_404(Input, pk=id)
    comments = Comment.objects.filter(input=input_data).order_by('-date_posted')
    data = {
        "comments": [
            {
                "id": comment.id,
                "author": comment.author.username,
                "input": comment.input.title,
                "message": comment.message,
                "category": comment.category.categoryName if comment.category else None,
                "date_posted": comment.date_posted
            }
            for comment in comments
        ]
    }
    return JsonResponse(data)


@login_required
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)

        if request.user == note.owner:
            note.delete()
            return JsonResponse({'message': 'The note has been deleted successfully.'})
        else:
            return JsonResponse({'error': 'You are not the owner of this note, so you cannot delete it.'}, status=403)

    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found.'}, status=404)
    


@login_required
def edit_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)

        if request.user == note.owner:
            if request.method == "POST":
                new_title = request.POST.get('title')
                new_content = request.POST.get('content')
                note.title = new_title
                note.content = new_content
                note.save()
                return JsonResponse({'message': 'The note has been edited successfully.'})

            return JsonResponse({'note_id': note.id, 'note_title': note.title, 'note_content': note.content,})

        return JsonResponse({'error': 'You are not the owner of this note, so you cannot edit it.'}, status=403)

    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found.'}, status=404)


def addNote(request, id, slug):
    if request.method == "POST":
        note_title = request.POST.get("note_title")
        note_content = request.POST.get("note_content")
        input_data = get_object_or_404(Input, pk=id)
        user = request.user
        category = input_data.category
        new_note = Note(title=note_title, content=note_content, input=input_data, owner=user, category=category)
        
        new_note.save()
    return HttpResponseRedirect(reverse("input", args=(id, slug)))



def addComment(request, id, slug):
    currentUser = request.user
    inputData = Input.objects.get(pk=id)
    categoryData = inputData.category
    message = request.POST['newComment']

    newComment = Comment(
        author = currentUser,
        input = inputData,
        message = message,
        category = categoryData,
    )
    newComment.save()
    return HttpResponseRedirect(reverse("input", args=(id, slug)))


@login_required
def edit_comment(request, id):
    try:
        comment = Comment.objects.get(id=id)

        if request.user == comment.author:
            if request.method == "POST":
                new_message = request.POST.get('message')
                comment.message = new_message
                comment.date_modified = timezone.now()
                comment.save()
                return JsonResponse({'message': 'The comment has been edited successfully.'})

            return JsonResponse({'comment_id': comment.id, 'comment_message': comment.message, 'date_modified': comment.date_modified.strftime("%b. %d, %Y, %I:%M %p")})

        return JsonResponse({'error': 'You are not the owner of this comment, so you cannot edit it.'}, status=403)

    except Note.DoesNotExist:
        return JsonResponse({'error': 'Comment not found.'}, status=404)



@login_required
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)

        if request.user == comment.author:
            comment.delete()
            return JsonResponse({'message': 'The comment has been deleted successfully.'})
        else:
            return JsonResponse({'error': 'You are not the owner of this comment, so you cannot delete it.'}, status=403)

    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found.'}, status=404)


def displayBookmark(request):
    if request.user.is_authenticated:
        currentUser = request.user
        selected_category = request.GET.get('category')
        categories = Category.objects.all()

        if selected_category:
            input = currentUser.inputBookmark.filter(category__categoryName=selected_category)
        else:
            input = currentUser.inputBookmark.all()
        return render(request, "capstone/bookmark.html", {
        "input": input,
        "categories": categories,
        "selected_category": selected_category
    })
    else:
        return HttpResponseRedirect(reverse("login"))


def removeBookmark(request, id, slug):
    inputData = Input.objects.get(pk=id)
    currentUser = request.user
    inputData.bookmark.remove(currentUser)
    return HttpResponseRedirect(reverse("input", args=(id, slug)))

def addBookmark(request, id, slug):
    inputData = Input.objects.get(pk=id)
    currentUser = request.user
    inputData.bookmark.add(currentUser)
    return HttpResponseRedirect(reverse("input", args=(id, slug)))



def displayCategory(request):
    category_name = request.GET.get('category')
    if category_name and category_name != "":
        category = get_object_or_404(Category, categoryName=category_name)
        activeInput = Input.objects.filter(isActive=True, category=category)
        selected_category = category_name
    else:
        activeInput = Input.objects.filter(isActive=True)
        selected_category = None

    return render(request, "capstone/displayCategory.html", {
        "input": activeInput,
        "categories": Category.objects.all(),
        "selected_category": selected_category
    })
    
    
def createInput(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "capstone/create.html", {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        category = request.POST["category"]
        currentUser = request.user

        categoryData = Category.objects.get(categoryName = category)


        newInput = Input(
            title = title,
            content = content,
            category = categoryData,
            owner = currentUser,
        )
        newInput.save()

        return HttpResponseRedirect(reverse("input", args=(newInput.id, slugify(newInput.title))))




def login_view(request):
    categories = Category.objects.all()
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password.",
                "categories": categories
            })
    else:
        return render(request, "capstone/login.html", {
            "categories": categories
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    categories = Category.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match.",
                "categories": categories
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken.",
                "categories": categories
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html", {
            "categories": categories 
        })
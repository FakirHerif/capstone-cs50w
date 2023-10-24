from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify

from .models import User, Category, Input, Comment, Site, Note


def index(request):
    activeInput = Input.objects.filter(isActive = True)
    allCategories = Category.objects.all()
    return render(request, "capstone/index.html", {
        "input": activeInput,
        "categories": allCategories
    })

def search(request):
    query = request.GET.get('query')
    if query:
        results = Input.objects.filter(title__icontains=query)
    else:
        results = Input.objects.none()
    return render(request, 'capstone/search_results.html', {'results': results, 'query': query})


def input(request, id, slug):
    inputData = Input.objects.get(pk=id)
    isInputInBookmark = request.user in inputData.bookmark.all()
    allComments = Comment.objects.filter(input=inputData)
    return render(request, "capstone/input.html", {
        "input": inputData,
        "isInputInBookmark": isInputInBookmark,
        "allComments": allComments
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


def displayBookmark(request):
    currentUser = request.user
    selected_category = request.GET.get('category')
    if selected_category:
        input = currentUser.inputBookmark.filter(category__categoryName=selected_category)
    else:
        input = currentUser.inputBookmark.all()
    categories = Category.objects.all()
    return render(request, "capstone/bookmark.html", {
        "input": input,
        "categories": categories,
        "selected_category": selected_category
    })

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
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")

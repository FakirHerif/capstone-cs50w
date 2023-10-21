from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Input, Comment


def index(request):
    activeInput = Input.objects.filter(isActive = True)
    allCategories = Category.objects.all()
    return render(request, "capstone/index.html", {
        "input": activeInput,
        "categories": allCategories
    })

def input(request, id):
    inputData = Input.objects.get(pk=id)
    isInputInBookmark = request.user in inputData.bookmark.all()
    allComments = Comment.objects.filter(input=inputData)
    return render(request, "capstone/input.html", {
        "input": inputData,
        "isInputInBookmark": isInputInBookmark,
        "allComments": allComments
    })


def addComment(request, id):
    currentUser = request.user
    inputData = Input.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        author = currentUser,
        input = inputData,
        message = message
    )

    newComment.save()

    return HttpResponseRedirect(reverse("input", args=(id, )))

def displayBookmark(request):
    currentUser = request.user
    input = currentUser.inputBookmark.all()
    return render(request, "capstone/bookmark.html", {
        "input": input
    })

def removeBookmark(request, id):
    inputData = Input.objects.get(pk=id)
    currentUser = request.user
    inputData.bookmark.remove(currentUser)
    return HttpResponseRedirect(reverse("input", args=(id, )))

def addBookmark(request, id):
    inputData = Input.objects.get(pk=id)
    currentUser = request.user
    inputData.bookmark.add(currentUser)
    return HttpResponseRedirect(reverse("input", args=(id, )))



def displayCategory(request):
    if request.method == "POST":
        CategoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=CategoryFromForm)
        activeInput = Input.objects.filter(isActive = True, category=category)
        allCategories = Category.objects.all()
        return render(request, "capstone/index.html", {
            "input": activeInput,
            "categories": allCategories
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
        url = request.POST["url"]
        sites = request.POST["sites"]
        category = request.POST["category"]
        currentUser = request.user

        categoryData = Category.objects.get(categoryName = category)


        newInput = Input(
            title = title,
            content = content,
            url = url,
            sites = sites,
            category = categoryData,
            owner = currentUser,
        )
        newInput.save()

        return HttpResponseRedirect(reverse(index))




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

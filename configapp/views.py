from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DeleteView

from .models import *
from .forms import *

def index(request):
    query = request.GET.get('q', '')  # Qidiruv so‘rovini olish
    news = News.objects.all()  # Barcha yangiliklarni olish
    categories = Categories.objects.all()  # Kategoriyalarni olish

    if query:
        news = news.filter(title__icontains=query)

    context = {
        "news": news,
        "categories": categories,
        "query": query
    }
    return render(request, 'index.html', context=context)

def categories(request,category_id):
    news = News.objects.filter(category_id=category_id)
    categories = Categories.objects.all()

    context = {
        "news":news,
        "categories":categories,
    }
    return render(request,'categories.html',context=context)

def new_about(request,new_id):
    new = News.objects.get(pk=new_id)
    categories = Categories.objects.all()

    context = {
        "new": new,
        "categories": categories,
    }
    return render(request, 'new_about.html', context=context)

def add_news(request):
    print(request)
    if request.method == "POST":
        form = NewsForm(request.POST,request.FILES)
        if form.is_valid():
            news = form.save()

            return redirect('home')
    else:
        form = NewsForm()
    return render(request, "add_news.html", {"form": form})

def add_categories(request):
    print(request)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            user = Categories.objects.create(**form.cleaned_data)
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, "add_categories.html", {"form": form})

def update_new(request,new_id):
    new = get_object_or_404(News,id=new_id)
    if request.method == "POST":
        form = NewsForm(request.POST,request.FILES,instance=new)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewsForm(instance=new)
    return render(request,'update_new.html',{'form':form,"new":new})


def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    error_message = ""
    form = UserLoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            error_message = "Login yoki parol noto‘g‘ri!"
    # else:
    #     form = UserLoginForm()
    return render(request,'login.html',{'form':form,'error_message': error_message})

def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    messages.success(request,f"{news_id} idli obyekt mavaffaqiyatli o'chirildi")
    return redirect('home')
def search_news(request):
    query = request.GET.get("q", "")
    results = list(News.objects.filter(title__icontains=query).values_list("id","title")[:5]) if query else []
    return JsonResponse({"results": results})
def LogoutPage(request):
    logout(request)
    return redirect('login')
from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LoginForm,AddPostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import blog_post
from django.contrib.auth.models import Group
# Home
def home(request):
    posts = blog_post.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})
# About
def about(request):
    return render(request, 'blog/about.html')
# Contact
def contact(request):
    return render(request, 'blog/contact.html')
# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = blog_post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')
# Logout

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# SignUp

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You have become an Auther')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html',{'form':form})

# Login

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login Successfully !! ')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddPostForm(request.POST)
            form.is_valid()
            form.save()
            form = AddPostForm()
        else:
            form = AddPostForm()
        return render(request, 'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = blog_post.objects.get(pk=id)
            form = AddPostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                form = AddPostForm()
        else:
            pi = blog_post.objects.get(pk=id)
            form = AddPostForm(instance=pi)
        return render(request, 'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = blog_post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
        else:
            return HttpResponseRedirect('/login/')



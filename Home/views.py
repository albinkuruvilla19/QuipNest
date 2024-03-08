from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .forms import QuipForm,SignUpForm,UpdateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User




# Create your views here.
def index(request):
    if request.user.is_authenticated:
        form = QuipForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                quip = form.save(commit=False)
                quip.user = request.user
                quip.save()
                messages.success(request,"Your Quip has been posted successfully.")
                return redirect('index')
        quips = Quips.objects.all().order_by("-created_at")
        return render(request,'index.html',{"quips":quips,"form":form})
    else:
        quips = Quips.objects.all().order_by("-created_at")
        return render(request,'index.html',{"quips":quips})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request,'profile_list.html',{"profiles":profiles})
    else:
        messages.success(request,"you must be logged in to view this page...")
        return redirect('index')
    
def profile(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        quips = Quips.objects.filter(user_id = pk)
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request,"profile.html",{"profile":profile,"quips":quips})
    else:
        messages.success(request,"you must be logged in to view this page...")
        return redirect('index')
    
def loginn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in!!")
            return redirect('index')
        else:
            messages.success(request,"There was an error logging in.Please try again.")
            return redirect('login')
    else:
        return render(request,"login.html")

    

def logoutt(request):
    logout(request)
    messages.success(request,"You have been logged out!")
    return redirect('login')

def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['femail']

            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You have successfully registered.")
            return redirect('login')

    
    return render(request,"register.html",{"form":form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = UpdateUserForm(request.POST or None,instance=current_user)
        if form.is_valid():
            form.save()
            login(request,current_user)
            messages.success(request,"Your information has been updated.")
            return redirect('index')
        return render(request,"update_user.html",{"form":form})
    else:
        messages.success(request,"You must be logged in.")
        return redirect('index')
    
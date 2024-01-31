from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.hashers import make_password


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        try:
            email =  request.POST.get('email') 
            password = request.POST.get('password') 
            confirm_password =  request.POST.get('confirm_password') 
            
            #email =  request.POST['email']
            #password = request.POST['password'] 
            #confirm_password = request.POST['confirm_password']

            user_obj = User.objects.filter(email = email)
            if user_obj.exists():
                messages.warning(request, "*** Account Already Exists ***")
                return redirect('/signup/')

            if password != confirm_password:
                messages.warning(request, "*** Passwords Didn't Matched ***")
                return redirect('/signup/')

            user_obj = User.objects.create(username = email, email = email)
            user_obj.set_password(password)
            user_obj.save()

            #password = make_password(password)
            #user_obj = User(email = email, password = password)
            #user_obj.save()
            
            messages.success(request, "*** Account Created ***")
            return redirect('/signin/')
        
        except Exception as ex:
            print(ex)
            messages.warning(request, "*** Something Went Wrong ***")
            return redirect('/signup/')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')

            user_obj = User.objects.filter(email = email)
            if not user_obj.exists():
                messages.warning(request, "*** User Not Found ***")
                return redirect('/signup/')
            
            user_obj = authenticate(request, username = email, email = email, password = password)
            if user_obj:
                login(request, user_obj)
                return redirect('/')
            else:
                messages.warning(request, "Incorrect Password")
                return redirect('/signin/')
        
        except Exception as ex:
            print(ex)
            messages.warning(request, "*** Something Went Wrong ***")
            return redirect('/signin/')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('/')
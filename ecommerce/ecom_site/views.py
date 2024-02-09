from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from math import ceil
#from django.contrib.auth.hashers import make_password


def index(request):

    allproducts = []

    prod_cate = Product.objects.values('category', 'category_id')
    cates = {item['category'] for item in prod_cate}
    for cate in cates:
        products = Product.objects.filter(category = cate)
        n = len(products)
        ncards = n // 4 + ceil((n / 4) - (n // 4))
        allproducts.append([products, range(1, ncards), ncards])

    context = {'allproducts' : allproducts}

    return render(request, 'index.html', context)


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
                messages.warning(request, "Account Already Exists")
                return redirect('/signup/')

            if password != confirm_password:
                messages.warning(request, "Passwords Didn't Matched")
                return redirect('/signup/')

            user_obj = User.objects.create(username = email, email = email)
            user_obj.set_password(password)
            user_obj.save()

            #password = make_password(password)
            #user_obj = User(email = email, password = password)
            #user_obj.save()
            
            messages.success(request, "Account Created")
            return redirect('/signin/')
        
        except Exception as ex:
            print(ex)
            messages.warning(request, "Something Went Wrong")
            return redirect('/signup/')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')

            user_obj = User.objects.filter(email = email)
            if not user_obj.exists():
                messages.warning(request, "User Not Found")
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
            messages.warning(request, "Something Went Wrong")
            return redirect('/signin/')

    return render(request, 'signin.html')


def signout(request):

    logout(request)
    return redirect('/')


def contact(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        messg = request.POST.get('message')

        details = Contact(name = name, email = email, subject = subject, messg = messg)
        details.save()
        
        messages.success(request, "Message has been sent, we will get back to you soon.")
        return redirect('/contact/')
    
    return redirect('/contact/')
    

def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(uid = product_id)
    cart, _ = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_items = CartItems.objects.create(
        cart = cart,
        product = product
    )
    return redirect('/')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from math import ceil
#from django.contrib.auth.hashers import make_password


def index(request):

    allproducts = []

    prod_cate = Product.objects.values('category')  #, 'category_id')
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
    

def add_to_cart(request, uid):
    user = request.user
    product = Product.objects.get(uid = uid)
    cart, created = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_item = CartItem.objects.create(cart = cart, product = product)
    return redirect('/')


def cart(request):
    try:
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
        cart = None

    """response = api.payment_request_create(
        amount = cart.order_total(),
        purpose = "Order",
        buyer_name = request.user.username,
        email = "gaurav714@gmail.com",
        redirect_url = "http://127.0.0.1:8000/success/"
    )
    context = {'cart' : cart, 'payment_url' : response['payment_request']['longurl']}"""

    return render(request, 'cart.html', {'cart' : cart})


def remove_cart_item(request, cart_item_uid):
    CartItem.objects.get(uid = cart_item_uid).delete()
    return redirect('/cart/')
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('signup/', signup, name = 'signup'),
    path('signin/', signin, name = 'signin'),
    path('signout/', signout, name = 'signout'),
    path('contact/', contact, name = 'contact'),
    path('add-to-cart/<uid>', add_to_cart, name = 'add_to_cart'),
    path('cart/', cart, name = 'cart'),
    path('remove_cart_item/<cart_item_uid>', remove_cart_item, name = 'remove_cart_item'),
    
]

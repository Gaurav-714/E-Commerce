from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('signup/', signup, name = 'signup'),
    path('signin/', signin, name = 'signin'),
    path('signout/', signout, name = 'signout'),
    path('contact/', contact, name = 'contact'),
    
]

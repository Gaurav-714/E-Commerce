from django.contrib import admin
from .models import *

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(CartItems)
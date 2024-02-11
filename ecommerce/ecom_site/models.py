from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class BaseModel(models.Model):
    uid = models.UUIDField(default = uuid4, editable = False, primary_key = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)

    class Meta:
        abstract = True


class ProductCategory(BaseModel):
    category = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.category
    

class Product(BaseModel):
    #product_id = models.UUIDField(default = uuid4, editable = False)
    category = models.ForeignKey(ProductCategory, on_delete = models.CASCADE, related_name = 'product', default = "")
    product_name = models.CharField(max_length = 100)
    desc = models.TextField(max_length = 300)
    price = models.IntegerField(default = 100)
    image = models.ImageField(upload_to = 'products', default = "")

    def __str__(self) -> str:
        return self.product_name
    

class Contact(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    subject = models.TextField(max_length = 100)    
    messg = models.TextField(max_length = 500)

    def __str__(self):
        return self.name
    

class Cart(BaseModel):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.SET_NULL, related_name = "cart")
    is_paid = models.BooleanField(default = False)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, related_name = "cart_item")
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    
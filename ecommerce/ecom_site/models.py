from django.db import models
import uuid
from ckeditor.fields import RichTextField


class BaseModel(models.Model):
    uid = models.UUIDField(default = uuid.uuid4, editable = False, primary_key = True)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)

    class Meta:
        abstract = True


class ProductCategory(BaseModel):
    category = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.category
    

class Product(BaseModel):
    category = models.ForeignKey(ProductCategory, on_delete = models.CASCADE, related_name = 'product')
    name = models.CharField(max_length =  100)
    desc = RichTextField()
    price = models.IntegerField(default = 100)
    image = models.ImageField(upload_to = 'products')

    def __str__(self) -> str:
        return self.name
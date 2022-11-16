from django.db import models
import uuid
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_slug = models.SlugField(max_length=100, unique=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        return reverse("product_by_category", args=[self.category_slug])  

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    product_slug = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/', default='product_images/Product-Image-Coming-Soon.jpg')
    product_price = models.FloatField()
    available_product_count = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        return self.product_name
    

class ProductImageGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product_images/')
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)


    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'product image gallery'
        verbose_name_plural = 'product image gallery'
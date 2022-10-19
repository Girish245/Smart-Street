from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_slug": ('category_name',)}


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"product_slug": ('product_name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

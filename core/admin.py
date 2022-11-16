from django.contrib import admin
from .models import Category, Product, ProductImageGallery
import admin_thumbnails

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_slug": ('category_name',)}

@admin_thumbnails.thumbnail('images')
class ProductImageInline(admin.TabularInline):
    model = ProductImageGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"product_slug": ('product_name',)}
    inlines = [ProductImageInline]

    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImageGallery)

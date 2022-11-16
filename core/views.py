from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImageGallery
from django.db.models import Q
from django.core.paginator import Paginator


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'core/index.html', context)


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, category_slug=category_slug) # the first category_slug is from the model and the second is from the urls.py
        products = Product.objects.filter(category=categories)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {'products': products}
    return render(request, 'core/store.html', context)


def searchProduct(request):

    if 'query' in request.GET:
        query = request.GET['query']
        if query:
            products = Product.objects.filter(Q(product_name__icontains=query)|Q(description__icontains=query)|Q(category__category_name__icontains=query))
        else:
            products = Product.objects.all() #or products = Product.objects.none()
        
    context = {'products': products}

    return render(request,'core/store.html', context)


def productDetails(request, pk):
    product = Product.objects.get(id=pk)
    product_gallery = ProductImageGallery.objects.filter(product=product)
    context = {'product': product, 'product_gallery': product_gallery}
    return render(request, 'core/product-details.html', context)
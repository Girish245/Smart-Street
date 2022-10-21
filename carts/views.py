from itertools import product
from statistics import quantiles
from django.shortcuts import render, redirect
from carts.models import CartItem
from core.models import Product



def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            user=request.user,
            product = product,
            quantity = 1,
        )
        cart_item.save()

    return redirect('cart')

#This will remove the item quantity and remove the product when the item quantity is less than 1
def remove_cart_item(request, pk):
    product = Product.objects.get(id=pk)
    cart_item = CartItem.objects.get(user=request.user, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

#This will remove the product when clicking the Remove button
def removeCart(request, pk):
    product = Product.objects.get(id=pk)
    cart_item = CartItem.objects.get(user=request.user, product=product)
    cart_item.delete()
    return redirect('cart')


def cart(request):
    
    cart_item = CartItem.objects.filter(user=request.user)
    gross = 0
    total = 0
    for item in cart_item:
        total += item.sub_total()
    tax = (total * (2/100))
    gross = total + tax
    context = {
        'cart_item': cart_item, 
        'total': total,
        'gross': gross,
        'tax': tax
        }
    return render(request, 'carts/cart.html', context)
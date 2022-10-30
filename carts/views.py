from django.shortcuts import render, redirect
from carts.models import CartItem
from core.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        if cart_item.quantity >= cart_item.product.available_product_count:
            messages.warning(request, "Available product count exceeded")
        else:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Product quantity increased successfully!")
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            user=request.user,
            product = product,
            quantity = 1,
        )
        cart_item.save()
        messages.success(request, "Product added to cart successfully!")

    return redirect('cart')

#This will remove the item quantity and remove the product when the item quantity is less than 1
@login_required(login_url='login')
def remove_cart_item(request, pk):
    product = Product.objects.get(id=pk)
    cart_item = CartItem.objects.get(user=request.user, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.warning(request, "Product quantity decreased successfully!")
    else:
        cart_item.delete()
        messages.warning(request, "Product removed from cart successfully.")
    return redirect('cart')

#This will remove the product when clicking the Remove button
@login_required(login_url='login')
def removeCart(request, pk):
    product = Product.objects.get(id=pk)
    cart_item = CartItem.objects.get(user=request.user, product=product)
    cart_item.delete()
    messages.warning(request, "Product removed from cart successfully.")
    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    
    cart_item = CartItem.objects.filter(user=request.user)
    cart_count =cart_item.count()
    gross_total = 0
    total = 0
    for item in cart_item:
        total += item.sub_total()
    tax = (total * (2/100))
    gross_total = total + tax
    context = {
        'cart_item': cart_item, 
        'total': total,
        'gross_total': gross_total,
        'tax': tax,
        'cart_count': cart_count,
        }
    return render(request, 'carts/cart.html', context)

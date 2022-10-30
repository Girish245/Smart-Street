from .models import CartItem

def cartCount(request):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(user=request.user)
        cart_count = cart_item.count()
        return {
            'cart_count': cart_count,
        }
    else:
        cart_count = 0
        return {
            'cart_count': cart_count,
        }

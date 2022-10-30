from django.shortcuts import render, redirect
from core.models import Product
from .forms import OrderAddress
from django.contrib.auth.decorators import login_required
from .models import Address, Order, Payment, OrderProduct
from carts.models import CartItem
import razorpay
import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))

@csrf_exempt
@login_required(login_url='login')
def payment(request):
    if request.method == "POST":
      
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print(params_dict)
            try:
                order = Order.objects.get(razorpay_order_id=razorpay_order_id)

            except:
                return HttpResponse("505 not found")
            result = client.utility.verify_payment_signature(params_dict)
            print(result)

            if result:
                order.is_ordered = True
                payment = Payment(
                    user = request.user,
                    razorpay_payment_id = payment_id,
                    razorpay_order_id = razorpay_order_id,
                    razorpay_signature = signature,
                    amount_paid = order.order_total,
                    status = "Completed",
                )
                payment.save()
                order.payment = payment
                order.razorpay_payment_id = payment_id
                order.razorpay_signature = signature
                order.status = 'Completed'
                order.save()
                    
                cart_items = CartItem.objects.filter(user=request.user)

                for item in cart_items:
                    order_product = OrderProduct()
                    order_product.order_id = order.id
                    order_product.payment = payment
                    order_product.user_id = request.user.id
                    order_product.product_id = item.product_id
                    order_product.quantity = item.quantity
                    order_product.product_price = item.product.product_price
                    order_product.ordered = True
                    order_product.save()

                    product = Product.objects.get(id=item.product.id)
                    product.available_product_count -= item.quantity
                    product.save()
                #remove item from the cart after successful payment 
                CartItem.objects.filter(user=request.user).delete()
                
                mail_subject = "Thank you for placing order"
                message = render_to_string('orders/order_placed_email.html', {
                    'user': request.user,
                    'order': order,
                })
                to_email = request.user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, 'Your order placed successfully!!')

                return redirect('profile')
                              
            else:
                order.is_ordered = False
                order.status = 'Canceled'
                order.save()
                return HttpResponse("Payment failed")
                # return HttpResponse("signature verification fails")

    else:
        return HttpResponseBadRequest('failed in else')



@login_required(login_url='login')
def billing_address(request):
    
    address = Address.objects.filter(user=request.user).exists()
    if address:
        address = Address.objects.get(user=request.user)
        form = OrderAddress(instance=address)
        if request.method == "POST":
            form = OrderAddress(request.POST, instance=address)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('place-order')
    else:
        form = OrderAddress()
        if request.method == "POST":
            form = OrderAddress(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('place-order')
    context = {'form': form}
    return render(request, 'orders/billing-address.html', context)



@login_required(login_url='login')
def place_order(request):
    current_user = request.user
    address = Address.objects.get(user=current_user)
    cart_item = CartItem.objects.filter(user=request.user)
    cart_count =cart_item.count()
    gross_total = 0
    total = 0
    for item in cart_item:
        total += item.sub_total()
    tax = (2 * total/100)
    gross_total = total + tax

    if request.method == "POST":
        order, create = Order.objects.get_or_create(
            user= current_user,
            address = address,
            status = 'New',
            is_ordered = "False"
        )
        order.save()
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(order.id)
        order.order_number = order_number
        order.save()
        try:
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            amount = gross_total * 100

            data = { 
                "amount": amount, 
                "currency": "INR",
                "receipt": order.order_number,
                 
                }

            payment = client.order.create(data=data)
            order.razorpay_order_id = payment["id"]
            order.order_total = gross_total
            order.save()

        except:
            pass
        context = {
        'cart_item': cart_item, 
        'total': total,
        'gross_total': gross_total,
        'tax': tax,
        'cart_count': cart_count,
        'address': address,
        'order': order,
        'payment': payment,
        }
        return render(request, 'orders/payment.html', context)

    context = {
        'cart_item': cart_item, 
        'total': total,
        'gross_total': gross_total,
        'tax': tax,
        'cart_count': cart_count,
        'address': address,
        }
    return render(request, 'orders/place-order.html', context)

@login_required(login_url='login')
def orderComplete(request, pk):
    user = request.user
    order = Order.objects.get(id=pk) 
    order_product = OrderProduct.objects.filter(order_id=order.id)
    sub_total = 0
    for price in order_product:
        p = price.product_price * price.quantity
        sub_total += p
    context = {'order_product': order_product, 'sub_total': sub_total}
    return render(request, 'orders/order-complete.html', context)




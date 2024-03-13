from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem
@login_required
def order_create_view(request):
    coupons_discount = {'123456789' : 30, '987654321' : 50}
    order_form = OrderForm()
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('home')

    if request.method == 'POST':
        order_form = OrderForm(request.POST, )

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            if cart.coupon:
                order_obj.coupon = cart.coupon
                if str(cart.coupon) in coupons_discount:
                    order_obj.discount = int(coupons_discount[str(cart.coupon)])
                else:
                    order_obj.discount = cart.coupon.discount
            order_obj.save()

            for item in cart:
                course = item['course_obj']
                if len(cart) == 1 and course.price==0:
                    OrderItem.objects.create(
                        order=order_obj,
                        course=course,
                        quantity=item['quantity'],
                        price=course.price,
                    )
                    return redirect('my_course')
                else:
                    OrderItem.objects.create(
                        order=order_obj,
                        course=course,
                        quantity=item['quantity'],
                        price=course.price,
                    )

            cart.clear()
            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

            request.session['order_id'] = order_obj.id
            return redirect('payment:go-to-gateway')

    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': order_form,
    })


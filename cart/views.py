from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from app.models import Course
from coupons.forms import CouponApplyForm
from orders.models import OrderItem
from .cart import Cart
from .forms import AddToCartCourseForm
# Create your views here.

def cart_detail_view(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        for item in cart:
            course = item['course_obj']
            course_id = Course.objects.get(slug=course.slug)
            if OrderItem.objects.filter(order__user=request.user, course=course_id).exists():
                cart.clear()
                return redirect('home')

        else:
            for item in cart:
                item['course_update_quantity_form'] = AddToCartCourseForm(initial={
                    'quantity': item['quantity'],
                    'inplace': True,
                })
            coupon_apply_form = CouponApplyForm()
            return render(request, 'cart/cart_detail.html', {
                'coupon_apply_form': coupon_apply_form,
                'cart': cart,
            })
    else:
        for item in cart:
            item['course_update_quantity_form'] = AddToCartCourseForm(initial={
                'quantity': item['quantity'],
                'inplace': True,
            })

        coupon_apply_form = CouponApplyForm()


        return render(request, 'cart/cart_detail.html', {
            'coupon_apply_form': coupon_apply_form,
            'cart': cart,
        }
                      )

@require_POST
def add_to_cart_view(request, course_slug):
    cart = Cart(request)

    course = get_object_or_404(Course, slug=course_slug)
    form = AddToCartCourseForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(course, quantity, replace_current_quantity=cleaned_data['inplace'])

    return redirect('cart:cart_detail')

def remove_from_cart(request, course_slug):
    cart = Cart(request)

    product = get_object_or_404(Course, slug=course_slug)

    cart.remove(product)

    return redirect('cart:cart_detail')

@require_POST
def clear_cart(request):
    cart = Cart(request)

    if len(cart):
        cart.clear()
        messages.success(request, 'All products successfully removed from your cart')
    else:
        messages.warning(request, 'Your cart is already empty')

    return redirect('home')








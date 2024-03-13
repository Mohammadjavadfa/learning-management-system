from django.contrib import messages
from decimal import Decimal
from app.models import Course
from coupons.models import Coupon

class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request

        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

        self.coupon_id = self.session.get("coupon_id")

    def add(self, course, quantity=1, replace_current_quantity=False):
        """
        Add the specified product to the cart if it exists
        """
        course_slug = str(course.slug)

        if course_slug not in self.cart:
            self.cart[course_slug] = {'quantity': 0}

        if replace_current_quantity:
            self.cart[course_slug]['quantity'] = quantity
        else:
            self.cart[course_slug]['quantity'] += quantity

        messages.success(self.request, 'Product successfully added to cart')

        self.save()

    def remove(self, course):
        """
        Remove a product from the cart
        """
        course_slug = str(course.slug)

        if course_slug in self.cart:
            del self.cart[course_slug]
            messages.success(self.request, 'Product successfully removed from cart')
            self.save()

    def save(self):
        """
        Mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        course_slugs = self.cart.keys()
        courses = Course.objects.filter(slug__in=course_slugs)

        cart = self.cart.copy()

        for course in courses:
            cart[str(course.slug)]['course_obj'] = course

        for item in cart.values():
            item['total_price'] = item['course_obj'].price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        product_ids = self.cart.keys()

        return sum(item['quantity'] * item['course_obj'].price for item in self.cart.values())

    def is_empty(self):
        if self.cart:
            return False
        return True

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()




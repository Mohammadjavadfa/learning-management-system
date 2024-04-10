from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db import models
from django.conf import settings
from app.models import Course
from coupons.models import Coupon

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=700)
    order_notes = models.CharField(max_length=700, blank=True)
    coupon = models.ForeignKey(Coupon, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_price_after_discount(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        total_cost = ((100-self.discount) / Decimal(100)) * total_cost
        return total_cost

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'OrderItem {self.id}: {self.course} x {self.quantity} (price:{self.price})'

    def get_cost(self):
        temp = self.price * self.quantity
        return temp - temp * (self.course.discount / Decimal(100))




from django.urls import path

from .views import cart_detail_view, add_to_cart_view, remove_from_cart, clear_cart

app_name = 'cart'

urlpatterns = [
    path('', cart_detail_view, name='cart_detail'),
    path('add/<slug:course_slug>/', add_to_cart_view, name='cart_add'),
    path('remove/<slug:course_slug>/', remove_from_cart, name='cart_remove'),
    path('clear/', clear_cart, name='cart_clear'),
]



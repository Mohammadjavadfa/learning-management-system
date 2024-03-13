from django.urls import path
from payment.views import go_to_gateway_view

app_name='payment'

urlpatterns = [
    path('go-to-gateway/', go_to_gateway_view, name='go-to-gateway'),
]


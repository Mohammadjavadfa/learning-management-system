from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from orders.models import Order
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
def go_to_gateway_view(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    toman_total_price = (order.get_total_price_after_discount())*10
    user_mobile_number = '+989112221234'

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create()
        bank.set_request(request)
        bank.set_amount(toman_total_price)

        bank.set_client_callback_url('/callback-gateway')
        bank.set_mobile_number(user_mobile_number)

        bank_record = bank.ready()

        return bank.redirect_gateway()
    except AZBankGatewaysException as e:

        # TODO: redirect to failed page.
        raise e

def callback_gateway_view(request):

    current_user = request.user
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        raise Http404


    if bank_record.is_success:
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.is_paid = True
        # store the unique transaction id
        order.transaction_id = tracking_code
        order.save()
        return HttpResponse("پرداخت با موفقیت انجام شد.")


    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")

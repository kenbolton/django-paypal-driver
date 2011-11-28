
from decimal import Decimal

from cartridge.shop.checkout import CheckoutError

from paypal.driver import PayPal
from paypal.models import PayPalResponse


def process(request, order_form, order):
    """
    Raise cartridge.shop.checkout.CheckoutError("error message") if
    payment is unsuccessful.
    - DoDirectPayment(self, acct, expdate, cvv2, cardtype, first_name, 
        last_name, amount, currency = "USD", **kwargs)
        returns True or False
    """
    acct = order_form.cleaned_data['card_number'].replace(' ', '')
    expdate = order_form.cleaned_data['card_expiry_month'] + order_form.cleaned_data['card_expiry_year']
    cvv2 = order_form.cleaned_data['card_ccv']
    if order_form.cleaned_data['card_type'] == 'Mastercard':
        cardtype = 'MasterCard'
    else:
        cardtype = order_form.cleaned_data['card_type']
    amount = Decimal(order.total)
    try:
        ipaddress = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ipaddress = request.META['REMOTE_ADDR']
    card_name = order_form.cleaned_data['card_name']
    first_name = card_name.split()[:-1]
    last_name = card_name.split()[-1]
    street = order_form.cleaned_data['billing_detail_street']
    city = order_form.cleaned_data['billing_detail_city']
    state = order_form.cleaned_data['billing_detail_state']
    postcode = order_form.cleaned_data['billing_detail_postcode']
    country = order_form.cleaned_data['billing_detail_country']
    email = order_form.cleaned_data['billing_detail_email']
    s_first_name = order_form.cleaned_data['shipping_detail_first_name']
    s_last_name = order_form.cleaned_data['shipping_detail_last_name']
    shiptoname = s_first_name + ' ' + s_last_name
    s_street = order_form.cleaned_data['shipping_detail_street']
    s_city = order_form.cleaned_data['shipping_detail_city']
    s_state = order_form.cleaned_data['shipping_detail_state']
    s_postcode = order_form.cleaned_data['shipping_detail_postcode']
    s_country = order_form.cleaned_data['shipping_detail_country']
    s_phone = order_form.cleaned_data['shipping_detail_phone']
    invnum = str(order.id)
    p = PayPal()
    result = p.DoDirectPayment(acct, expdate, cvv2, cardtype, first_name, last_name,
            amount, currency = "USD", email=email, ipaddress=ipaddress, street=street,
            city=city, state=state, zip=postcode, countrycode=country,
            invnum=invnum, shiptoname=shiptoname, shiptostreet=s_street,
            shiptocity=s_city, shiptostate=s_state, shiptozip=s_postcode,
            shiptocountry=s_country, shiptophonenum=s_phone)
    if result == True:
        response = PayPalResponse()
        response.fill_from_response(p.GetPaymentResponse, action='Payment')
        response.status = PayPalResponse.get_default_status()
        response.save()
        order.status = '2'
        order.save()
    else:
        raise CheckoutError(p.apierror)



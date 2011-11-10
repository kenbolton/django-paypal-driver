# -*- coding: utf-8 -*-

from django.contrib import admin
from paypal.models import PayPalResponse, PayPalResponseStatus

class PayPalResponseAdmin(admin.ModelAdmin):
    list_display = (
                    'trans_id',
                    'status',
                    'token',
                    'currencycode',
                    'charged',
                    'payment_received',
                    'error_msg',
                    )
    list_filter = ("payment_received", "status")
    search_fields = ('token', 'trans_id')

admin.site.register(PayPalResponse, PayPalResponseAdmin)

# -*- coding: utf-8 -*-
"""Прави настройките за PayPal достъпни във всички шаблони."""
from django.conf import settings


def paypal(request):
    return {
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID,
        'PAYPAL_CURRENCY': settings.PAYPAL_CURRENCY,
    }

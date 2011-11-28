
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
    name="PAYPAL_USER",
    label=_("PayPal API Username"),
    description=_("Username for the PayPal API"),
    editable=True,
    default="",
)

register_setting(
    name="PAYPAL_PASSWORD",
    label=_("PayPal Password"),
    description=_("User password for the PayPal API"),
    editable=True,
    default="",
)

register_setting(
    name="PAYPAL_SIGNATURE",
    label=_("PayPal API Signature"),
    description=_("Signature key for the PayPal API"),
    editable=True,
    default="",
)

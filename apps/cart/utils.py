from django.conf import settings
from django.http import HttpRequest, HttpResponse

from apps.cart.models import Cart


async def get_or_create_cart_uuid(request: HttpRequest) -> tuple[str, bool]:
    """
    Gets the current cart or creates a new one
    """
    cart_uuid = request.get_signed_cookie(
        settings.CART_UUID_COOKIE_NAME, False, max_age=settings.CART_EXPIRES_AFTER_SECS
    )
    # Cart does not exist or has expired
    if not cart_uuid:
        cart = await Cart.objects.acreate()
        return str(cart.id), True
    return cart_uuid, False


def set_cart_uuid_cookie(response: HttpResponse, uuid: str) -> None:
    """
    Sets the ID and Max-Age
    """
    response.set_signed_cookie(
        settings.CART_UUID_COOKIE_NAME, uuid, max_age=settings.CART_EXPIRES_AFTER_SECS
    )

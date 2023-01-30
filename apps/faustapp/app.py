import logging
import os

import django
import faust
from asgiref.sync import sync_to_async
from django.conf import settings

from apps.faustapp.models import ItemRecord

logger = logging.getLogger(__name__)

os.environ.setdefault("FAUST_LOOP", "eventlet")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clearcode.settings")
django.setup()

app = faust.App("cc", broker=f"kafka://{settings.KAFKA_URL}")
items = app.topic(settings.KAFKA_STREAM_TOPIC, value_type=ItemRecord)

from apps.cart.models import Cart, Item  # noqa


@app.agent(items)
async def add_item(items_stream):
    """
    Adds items to a cart
    """
    async for item in items_stream:
        logger.info("Processing: %s", item)
        await update_cart(item)


async def update_cart(topic_item):
    try:
        cart = await Cart.objects.aget(id=topic_item.cart_uuid)
        item, _ = await Item.objects.aget_or_create(
            external_id=topic_item.external_id
        )
        # This will also update items in expired carts.
        # The requirements are too vague to implement any kind of version control :)
        if item.name != topic_item.name or item.value != topic_item.value:
            item.name = topic_item.name
            item.value = topic_item.value
            await sync_to_async(item.save)()
        await sync_to_async(cart.items.add)(item)
        await sync_to_async(cart.save)()
    except Cart.DoesNotExist as e:
        logger.error("Cart does not exist: PK=%s: %s", topic_item.cart_uuid, e)


if __name__ == "__main__":
    app.main()

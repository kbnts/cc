import io
import logging
from typing import Dict

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views import View
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from apps.cart import utils
from apps.cart.serializers import ItemSerializer
from clearcode.core import ItemPublisher, KafkaPublisher

logger = logging.getLogger(__name__)
item_publisher = ItemPublisher(client=KafkaPublisher())


class AddItemAPIView(View):
    """
    Note: DRF doesn't support async views yet, this endpoint inherits from Django's base *View*
    """

    item_topic = settings.KAFKA_STREAM_TOPIC
    serializer_class = ItemSerializer
    expected_content_type = "application/json"

    async def post(self, request: HttpRequest) -> HttpResponse:
        response = HttpResponse(status=status.HTTP_204_NO_CONTENT)

        # Bail if it's not a JSON request
        if not (content_type := request.META.get("HTTP_ACCEPT")) == self.expected_content_type:
            logger.warning("Wrong content type: %s", content_type)
            return response

        # Check if the request body is valid
        if not (validated_data := self.validated_data):
            return response

        # Get or create active cart
        cart_uuid, created = await utils.get_or_create_cart_uuid(self.request)
        if created:
            utils.set_cart_uuid_cookie(response, cart_uuid)

        # Publish data
        self.publish_item(validated_data, cart_uuid)
        return response

    def parse_body(self) -> Dict:
        try:
            stream = io.BytesIO(self.request.body)
            return JSONParser().parse(stream)
        except ParseError as e:
            logger.error("Unable to parse request data: %s=%s", self.request.body, e)
            return {}

    @property
    def validated_data(self) -> None | Dict:
        if not (data := self.parse_body()):
            return None

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            logger.error("Invalid request data: %s", serializer.errors)
            return None
        return serializer.data

    def publish_item(self, data: Dict, cart_uuid: str) -> None:
        data.update({"cart_uuid": cart_uuid})
        item_publisher.publish(topic=self.item_topic, data=data)

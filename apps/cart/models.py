import uuid

from django.db import models
from django.utils.translation import gettext as _


class Cart(models.Model):
    """
    Container for the Item model
    """

    id = models.UUIDField(
        verbose_name="UUID", primary_key=True, default=uuid.uuid4, editable=False
    )
    created_timestamp = models.DateTimeField(
        verbose_name=_("Created timestamp"), auto_now_add=True
    )

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        ordering = ("-created_timestamp",)


class Item(models.Model):
    external_id = models.CharField(
        verbose_name=_("Product ID of the item"), max_length=255, primary_key=True
    )
    name = models.CharField(
        verbose_name=_("Name of the item"), max_length=255, default="", blank=True
    )
    value = models.PositiveIntegerField(
        verbose_name=_("Value of the item (in cents)"), default=0
    )
    cart = models.ForeignKey(
        verbose_name=_("Cart"),
        to=Cart,
        related_name="items",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.value}".strip()

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

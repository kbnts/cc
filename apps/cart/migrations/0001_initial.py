# Generated by Django 4.1.5 on 2023-01-27 04:31

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "created_timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created timestamp"
                    ),
                ),
            ],
            options={
                "verbose_name": "Cart",
                "verbose_name_plural": "Carts",
                "ordering": ("-created_timestamp",),
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "external_id",
                    models.CharField(
                        max_length=255,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Product ID of the item",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="Name of the item",
                    ),
                ),
                (
                    "value",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Value of the item (in cents)"
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="items",
                        to="cart.cart",
                        verbose_name="Cart",
                    ),
                ),
            ],
            options={
                "verbose_name": "Item",
                "verbose_name_plural": "Items",
            },
        ),
    ]

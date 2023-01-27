from django.contrib import admin

from apps.cart.models import Cart, Item

admin.site.register(Item)
admin.site.register(Cart)

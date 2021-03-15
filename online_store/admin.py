from django.contrib import admin

# Register your models here.
from online_store.models import Product, ShoppingCart, ShoppingCartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "sale_start", "sale_end"]

    class Meta:
        model = Product


@admin.register(ShoppingCart)
class ShoppingCardAdmin(admin.ModelAdmin):
    list_display = ["name", "address"]

    class Meta:
        model = ShoppingCart


@admin.register(ShoppingCartItem)
class ShoppingCardItemAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity"]

    class Meta:
        model = ShoppingCartItem

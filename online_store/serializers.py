from online_store.models import Product, ShoppingCartItem
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'quantity')


class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description',
                  'price', 'sale_start', 'sale_end', 'is_on_sale', 'current_price',
                  'cart_items')

    # def to_representation(self, instance):
        #     data = super().to_representation(instance)
        #     data["is_on_sale"] = instance.is_on_sale()
        #     data["current_price"] = instance.current_price()
        #     return data

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data

    # from rest_framework.renderers import JSONRenderer
    # product = Product.objects.all()[0]
    # data = serializer.to_representation(product)
    # renderer = JSONRenderer()
    # print(renderer.render(data))

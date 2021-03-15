from online_store.models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description',
                  'price', 'sale_start', 'sale_end')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["is_on_sale"] = instance.is_on_sale()
        data["current_price"] = instance.current_price()
        return data


# from rest_framework.renderers import JSONRenderer
# product = Product.objects.all()[0]
# data = serializer.to_representation(product)
# renderer = JSONRenderer()
# print(renderer.render(data))

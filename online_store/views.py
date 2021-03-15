from django.shortcuts import render, HttpResponse
from online_store.serializers import ProductSerializer
from online_store.models import Product
from rest_framework.renderers import JSONRenderer
# Create your views here.


def productCihatDemo(request):
    products = Product.objects.all()
    serializer = ProductSerializer()
    data = map(lambda product: serializer.to_representation(product), products)
    renderer = JSONRenderer()
    return HttpResponse(renderer.render(data))

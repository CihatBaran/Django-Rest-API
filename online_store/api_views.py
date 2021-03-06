from online_store.models import Product
from online_store.serializers import ProductSerializer, ProductStatSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone


from rest_framework.exceptions import ValidationError


class ProductPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ProductList(ListAPIView):
    # queryset
    queryset = Product.objects.all()
    # class
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    # filters
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['id']
    search_fields = ["name", "description"]

    def get_queryset(self):
        on_sale = self.request.query_params.get("on_sale", None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Product.objects.all()

        if on_sale.lower() == "true":
            now = timezone.now()
            return queryset.filter(sale_start__lte=now, sale_end__gte=now)
        elif on_sale.lower() == "false":
            now = timezone.now()
            return queryset.exclude(sale_start__lte=now, sale_end__gte=now)


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):

        try:
            price = request.data.get('price')
            sale_start_date = request.data.get('sale_start')
            sale_end_date = request.data.get('sale_end')

            if sale_end_date < sale_start_date:
                raise ValidationError(
                    {'sale_end': 'sale end cannot be earlier than sale start'})

            if price is not None and float(price) <= 0.0:
                raise ValidationError(
                    {'price': 'price must be above 0 dollars'})
        except ValueError:
            raise ValidationError({'price': 'price should be a number'})

        return super().create(request, *args, **kwargs)


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete(f"product_data_{product_id}")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            product = response.data
            cache.set(f"product_data_{product['id']}", {
                'name': product['name'],
                'description': product['description'],
                'price': product['price'],
            })
        return response


class ProductStatAPIView (GenericAPIView):
    lookup_field = 'id'
    serializer_class = ProductStatSerializer
    queryset = Product.objects.all()

    def get(self, request, format=None, id=None):
        obj = self.get_object()
        serializer = ProductStatSerializer({
            'stats': {
                '2019-01-01': [5, 10, 15],
                '2019-01-02': [1, 54, 33],
            }
        })
        return Response(serializer.data)

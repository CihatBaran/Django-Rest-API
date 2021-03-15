from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination


from online_store.serializers import ProductSerializer
from online_store.models import Product


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
    search_fields = ["=name", "description"]

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
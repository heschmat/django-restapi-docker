from django.shortcuts import get_object_or_404
from django.http import JsonResponse


from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import (
    ProductSerializer,
    OrderSeializer
)
from api import models


@api_view(['GET'])
def product_list(request):
    products = models.Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


def product_detail(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    serializer = ProductSerializer(product)
    return JsonResponse({'data': serializer.data})


@api_view(['GET'])
def order_list(request):
    orders = models.Order.objects.all()
    serializer = OrderSeializer(orders, many=True)
    return Response(serializer.data)

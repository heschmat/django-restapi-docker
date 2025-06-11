from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum  # Max, ...

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework.views import APIView

from api.serializers import (
    ProductSerializer,
    OrderSeializer,
    OrderInfoSerializer,
    StockInfoSerializer,
)
from api import models


# class ProductListAPIView(generics.ListAPIView):
#     # Only show products that are available (stock > 0)
#     queryset = models.Product.objects.filter(stock__gt=100)
#     # queryset = models.Product.objects.exclude(stock__lte=100)

#     serializer_class = ProductSerializer


# class ProductCreateAPIView(generics.CreateAPIView):
#     queryset = models.Product
#     serializer_class = ProductSerializer

#     # We're not doing anything here;
#     # just to showcase we can overwrite the methods. and what `request.data` look like.
#     # for exampl, it includes csrf token as well.
#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request, *args, **kwargs)


# or simply:
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        # Only admin user can post a new product.
        if self.request.method == 'POST':
            self.permission_classes = [ IsAdminUser ]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

# @api_view(['GET'])
# def product_list(request):
#     products = models.Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


# def product_detail(request, pk):
#     product = get_object_or_404(models.Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return JsonResponse({'data': serializer.data})


@api_view(['GET'])
def order_list(request):
    orders = models.Order.objects.all()
    serializer = OrderSeializer(orders, many=True)
    return Response(serializer.data)


class UserOrderListAPIView(generics.ListAPIView):
    queryset = models.Order.objects.all()
    serializer_class = OrderSeializer
    permission_classes = [ IsAuthenticated ]

    def get_queryset(self):
        qs = super().get_queryset()
        # self.request.user refers to the authenticated user.
        return qs.filter(user=self.request.user)


@api_view(['GET'])
def order_info(request):
    orders = models.Order.objects.all()
    cancelled_orders = orders.filter(status=models.Order.StatusChoices.CANCELLED).count()
    confirmed_orders = orders.filter(status=models.Order.StatusChoices.CONFIRMED).count()

    # Total revenue is sum of all order items: price * quantity
    total_revenue = 0
    for order in orders:
        for item in order.items.all():
            total_revenue += item.order_item_sum

    total_orders = orders.count()
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0

    serializer = OrderInfoSerializer({
        'total_orders': total_orders,
        'cancelled_orders': cancelled_orders,
        'confirmed_orders': confirmed_orders,
        'total_revenue': total_revenue,
        'average_order_value': average_order_value,
    })

    return Response(serializer.data)


# @api_view(['GET'])
# def stock_info(request):
#     products = models.Product.objects.all()

#     total_products = products.count()
#     products_in_stock = products.filter(stock__gt=0).count()
#     out_of_stock_products = products.filter(stock=0).count()
#     total_stock_quantity = products.aggregate(total=Sum('stock'))['total'] or 0

#     serializer = StockInfoSerializer({
#         'total_products': total_products,
#         'products_in_stock': products_in_stock,
#         'out_of_stock_products': out_of_stock_products,
#         'total_stock_quantity': total_stock_quantity,
#     })

#     return Response(serializer.data)


class StockInfoAPIView(APIView):
    def get(self, request):
        products = models.Product.objects.all()

        total_products = products.count()
        products_in_stock = products.filter(stock__gt=0).count()
        out_of_stock_products = products.filter(stock=0).count()
        total_stock_quantity = products.aggregate(total=Sum('stock'))['total'] or 0

        serializer = StockInfoSerializer({
            'total_products': total_products,
            'products_in_stock': products_in_stock,
            'out_of_stock_products': out_of_stock_products,
            'total_stock_quantity': total_stock_quantity,
        })

        return Response(serializer.data)

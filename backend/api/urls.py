from django.urls import path

from . import views


urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:product_id>', views.ProductDetailAPIView.as_view()),
    path('orders/', views.order_list),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),
    path('orders-info/', views.order_info),
    path('stocks-info/', views.stock_info),
]

from rest_framework import serializers

from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'stock'
        )

    # We can add flield-level validation via `.validate_*` mthods.
    def validate_price(self, value):
        """Makes sure price is non-negative."""
        if value <= 0:
            raise serializers.ValidationError('price must be positive value.')
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price', max_digits=5, decimal_places=2)

    class Meta:
        model = OrderItem
        # fields = ('product', 'quantity')
        fields = ('product_name', 'product_price', 'quantity', 'order_item_sum')


class OrderSeializer(serializers.ModelSerializer):
    # `items` is the `related_name` we gave to `order` field in `OrderItem` class/table.
    items = OrderItemSerializer(many=True, read_only=True)

    total_sum = serializers.SerializerMethodField()
    # method name convension: get_<field>
    def get_total_sum(self, obj):
        order_items = obj.items.all()
        return sum(itm.order_item_sum for itm in order_items)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_sum'
        )

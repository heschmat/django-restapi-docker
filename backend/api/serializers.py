from rest_framework import serializers

from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock')

    # We can add flield-level validation via `.validate_*` mthods.
    def validate_price(self, value):
        """Makes sure price is non-negative."""
        if value <= 0:
            raise serializers.ValidationError('price must be positive value.')
        return value

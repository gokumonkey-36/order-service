from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product_name', 'product_price', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'session_id', 'items', 'total', 'created_at']

    def get_total(self, obj):
        return obj.get_total()


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=200)
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1, default=1)


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'product_price', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'session_id', 'status', 'total_amount',
            'customer_name', 'customer_email', 'shipping_address',
            'phone', 'items', 'created_at'
        ]


class CheckoutSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    customer_name = serializers.CharField(max_length=200)
    customer_email = serializers.EmailField()
    shipping_address = serializers.CharField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
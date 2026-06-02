from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer, AddToCartSerializer,
    OrderSerializer, CheckoutSerializer
)


class CartViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        """GET /api/orders/cart/{session_id}/"""
        cart, _ = Cart.objects.get_or_create(session_id=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add(self, request, pk=None):
        """POST /api/orders/cart/{session_id}/add/"""
        cart, _ = Cart.objects.get_or_create(session_id=pk)
        serializer = AddToCartSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=data['product_id'],
            defaults={
                'product_name': data['product_name'],
                'product_price': data['product_price'],
                'quantity': data['quantity'],
            }
        )

        if not created:
            item.quantity += data['quantity']
            item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='remove/(?P<item_id>[^/.]+)')
    def remove(self, request, pk=None, item_id=None):
        """DELETE /api/orders/cart/{session_id}/remove/{item_id}/"""
        cart = get_object_or_404(Cart, session_id=pk)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return Response(CartSerializer(cart).data)

    @action(detail=True, methods=['delete'])
    def clear(self, request, pk=None):
        """DELETE /api/orders/cart/{session_id}/clear/"""
        cart = get_object_or_404(Cart, session_id=pk)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'})


class OrderViewSet(viewsets.ViewSet):

    def list(self, request):
        """GET /api/orders/ — filter by session_id query param"""
        session_id = request.query_params.get('session_id')
        orders = Order.objects.prefetch_related('items').order_by('-created_at')
        if session_id:
            orders = orders.filter(session_id=session_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET /api/orders/{id}/"""
        order = get_object_or_404(Order, pk=pk)
        return Response(OrderSerializer(order).data)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """POST /api/orders/checkout/ — create order from cart"""
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        cart = get_object_or_404(Cart, session_id=data['session_id'])

        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            session_id=data['session_id'],
            total_amount=cart.get_total(),
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            shipping_address=data['shipping_address'],
            phone=data.get('phone', ''),
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_id=item.product_id,
                product_name=item.product_name,
                product_price=item.product_price,
                quantity=item.quantity,
            )

        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
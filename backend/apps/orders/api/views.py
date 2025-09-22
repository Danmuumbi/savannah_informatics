from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from .serializers import OrderSerializer, OrderCreateSerializer
from .tasks import send_order_sms, send_admin_email

class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Order.objects.all()
        return Order.objects.filter(customer__user=self.request.user)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create order
        order = Order.objects.create(
            customer=serializer.validated_data['customer'],
            status='pending'
        )
        
        total_amount = 0
        items_data = serializer.validated_data['items']
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Create order item
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            
            total_amount += order_item.subtotal
        
        order.total_amount = total_amount
        order.save()
        
        # Send notifications asynchronously
        send_order_sms.delay(order.id)
        send_admin_email.delay(order.id)
        
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Order.objects.all()
        return Order.objects.filter(customer__user=self.request.user)
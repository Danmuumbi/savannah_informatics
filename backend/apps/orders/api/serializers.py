from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = ['customer', 'items', 'notes']
    
    def validate_items(self, value):
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must contain product_id and quantity")
            
            try:
                product = Product.objects.get(id=item['product_id'])
                item['product'] = product
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {item['product_id']} does not exist")
        
        return value
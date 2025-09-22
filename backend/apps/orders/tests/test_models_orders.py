
import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apps.customers.models import Customer
from apps.products.models import Category, Product
from apps.orders.models import Order, OrderItem

User = get_user_model()

@pytest.mark.django_db
class TestOrderModel:
    @pytest.fixture
    def test_customer(self):
        user = User.objects.create_user(email='customer@test.com', password='testpass')
        return Customer.objects.create(user=user, phone_number='+254712345678')
    
    @pytest.fixture
    def test_product(self):
        category = Category.objects.create(name='Test Category')
        return Product.objects.create(
            name='Test Product',
            price=100.00,
            category=category,
            stock_quantity=10
        )
    
    def test_create_order(self, test_customer):
        """Test creating an order"""
        order = Order.objects.create(
            customer=test_customer,
            shipping_address='123 Test Street',
            total_price=0.00
        )
        
        assert order.customer == test_customer
        assert order.status == 'pending'
        assert str(order) == f'Order {order.id}'
    
    def test_create_order_item(self, test_customer, test_product):
        """Test creating an order item"""
        order = Order.objects.create(
            customer=test_customer,
            shipping_address='123 Test Street',
            total_price=0.00
        )
        
        order_item = OrderItem.objects.create(
            order=order,
            product=test_product,
            quantity=2,
            price=test_product.price
        )
        
        assert order_item.order == order
        assert order_item.product == test_product
        assert order_item.quantity == 2
        assert order_item.price == 100.00
        assert order_item.subtotal == 200.00
    
    def test_order_total_calculation(self, test_customer, test_product):
        """Test order total calculation"""
        order = Order.objects.create(
            customer=test_customer,
            shipping_address='123 Test Street',
            total_price=0.00
        )
        
        # Create multiple order items
        OrderItem.objects.create(
            order=order,
            product=test_product,
            quantity=2,
            price=test_product.price
        )
        
        another_product = Product.objects.create(
            name='Another Product',
            price=50.00,
            category=test_product.category,
            stock_quantity=5
        )
        
        OrderItem.objects.create(
            order=order,
            product=another_product,
            quantity=1,
            price=another_product.price
        )
        
        # Calculate total
        order.calculate_total()
        
        assert order.total_price == 250.00  # (2 * 100) + (1 * 50)
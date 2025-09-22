
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.customers.models import Customer
from apps.products.models import Category, Product
from apps.orders.models import Order, OrderItem

User = get_user_model()

@pytest.mark.django_db
class TestOrderViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def test_user(self):
        return User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    @pytest.fixture
    def test_customer(self, test_user):
        return Customer.objects.create(
            user=test_user,
            phone_number='+254712345678'
        )
    
    @pytest.fixture
    def test_product(self):
        category = Category.objects.create(name='Test Category')
        return Product.objects.create(
            name='Test Product',
            price=100.00,
            category=category,
            stock_quantity=10
        )
    
    @pytest.fixture
    def test_order(self, test_customer):
        return Order.objects.create(
            customer=test_customer,
            shipping_address='123 Test Street',
            total_price=100.00
        )
    
    def test_create_order_authenticated(self, api_client, test_user, test_customer, test_product):
        """Test creating an order as authenticated user"""
        api_client.force_authenticate(user=test_user)
        
        url = reverse('order-list')
        data = {
            'shipping_address': '123 Test Street',
            'items': [
                {
                    'product': test_product.id,
                    'quantity': 2
                }
            ]
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['customer'] == test_customer.id
        assert response.data['total_price'] == 200.00  # 2 * 100
    
    def test_list_orders_authenticated(self, api_client, test_user, test_order):
        """Test listing orders for authenticated user"""
        api_client.force_authenticate(user=test_user)
        
        url = reverse('order-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
    
    def test_create_order_unauthenticated(self, api_client, test_product):
        """Test that unauthenticated users cannot create orders"""
        url = reverse('order-list')
        data = {
            'shipping_address': '123 Test Street',
            'items': [
                {
                    'product': test_product.id,
                    'quantity': 2
                }
            ]
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
# backend/conftest.py
import pytest
from django.contrib.auth import get_user_model
from apps.customers.models import Customer
from apps.products.models import Category, Product

User = get_user_model()

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_customer(db, test_user):
    return Customer.objects.create(
        user=test_user,
        phone_number='+254712345678',
        address='123 Test Street'
    )

@pytest.fixture
def test_category(db):
    return Category.objects.create(
        name='Test Category',
        description='Test Description'
    )

@pytest.fixture
def test_product(db, test_category):
    return Product.objects.create(
        name='Test Product',
        description='Test Description',
        price=100.00,
        category=test_category,
        stock_quantity=10
    )
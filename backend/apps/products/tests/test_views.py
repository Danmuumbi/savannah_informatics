
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.products.models import Category, Product

@pytest.mark.django_db
class TestProductViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def sample_category(self):
        return Category.objects.create(name='Electronics')
    
    @pytest.fixture
    def sample_product(self, sample_category):
        return Product.objects.create(
            name='Test Laptop',
            description='Test Description',
            price=1000.00,
            category=sample_category,
            stock_quantity=5
        )
    
    def test_list_products(self, api_client, sample_product):
        """Test listing products"""
        url = reverse('product-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == sample_product.name
    
    def test_retrieve_product(self, api_client, sample_product):
        """Test retrieving a single product"""
        url = reverse('product-detail', kwargs={'pk': sample_product.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == sample_product.name
    
    def test_average_price_by_category(self, api_client, sample_category):
        """Test average price calculation for a category"""
        # Create products with different prices
        Product.objects.create(
            name='Product 1',
            price=100.00,
            category=sample_category,
            stock_quantity=5
        )
        Product.objects.create(
            name='Product 2',
            price=200.00,
            category=sample_category,
            stock_quantity=3
        )
        
        url = reverse('category-average-price', kwargs={'pk': sample_category.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['average_price'] == 150.00
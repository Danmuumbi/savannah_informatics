
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.customers.models import Customer


User = get_user_model()

@pytest.mark.django_db
class TestCustomerViews:
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
            phone_number='+254712345678',
            address='123 Test Street'
        )
    
    def test_get_customer_profile_authenticated(self, api_client, test_user, test_customer):
        """Test retrieving profile for authenticated user"""
        api_client.force_authenticate(user=test_user)
        url = reverse('customer-profile')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['phone_number'] == test_customer.phone_number
    
    def test_get_customer_profile_unauthenticated(self, api_client):
        """Test that authentication is required"""
        url = reverse('customer-profile')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_customer_profile(self, api_client, test_user, test_customer):
        """Test updating customer profile"""
        api_client.force_authenticate(user=test_user)
        url = reverse('customer-profile')
        data = {
            'phone_number': '+254798765432',
            'address': '456 Updated Street'
        }
        response = api_client.patch(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        test_customer.refresh_from_db()
        assert test_customer.phone_number == data['phone_number']

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from apps.customers.models import Customer

User = get_user_model()

@pytest.mark.django_db
class TestCustomerModel:
    def test_create_customer(self):
        """Test creating a customer is successful"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        customer = Customer.objects.create(
            user=user,
            phone_number='+254712345678',
            address='123 Test Street, Nairobi'
        )
        
        assert customer.user == user
        
     
        print(f"DEBUG: Customer __str__ returns: '{str(customer)}'")
        
     
        assert str(customer) == 'test@example.com'
        
    
    
    def test_customer_phone_validation(self):
        """Test customer phone number validation"""
        user = User.objects.create_user(
            username='testuser2', 
            email='test2@example.com',
            password='testpass123'
        )
        
        # Test invalid phone number
        with pytest.raises(ValidationError):
            customer = Customer(
                user=user,
                phone_number='invalid',
                address='123 Test Street'
            )
            customer.full_clean()
# backend/apps/products/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from apps.products.models import Category, Product

@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self):
        """Test creating a category"""
        category = Category.objects.create(
            name='Electronics',
            description='Electronic products'
        )
        
        assert category.name == 'Electronics'
        assert category.slug == 'electronics'
        assert str(category) == 'Electronics'
    
    def test_category_tree_structure(self):
        """Test category hierarchy"""
        electronics = Category.objects.create(name='Electronics')
        laptops = Category.objects.create(name='Laptops', parent=electronics)
        gaming_laptops = Category.objects.create(name='Gaming Laptops', parent=laptops)
        
        assert laptops.parent == electronics
        assert gaming_laptops in laptops.get_children()
        assert gaming_laptops in electronics.get_descendants()
        assert electronics.get_ancestors().count() == 0
        assert gaming_laptops.get_ancestors().count() == 2

@pytest.mark.django_db
class TestProductModel:
    @pytest.fixture
    def sample_category(self):
        return Category.objects.create(name='Test Category')
    
    def test_create_product(self, sample_category):
        """Test creating a product"""
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100.00,
            category=sample_category,
            stock_quantity=10
        )
        
        assert product.name == 'Test Product'
        assert product.price == 100.00
        assert product.category == sample_category
        assert str(product) == 'Test Product'
    
    def test_product_price_validation(self, sample_category):
        """Test product price validation"""
        with pytest.raises(ValidationError):
            product = Product(
                name='Invalid Product',
                price=-10.00,
                category=sample_category
            )
            product.full_clean()
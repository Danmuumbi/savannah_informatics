from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Q
from apps.products.models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['GET'])
def category_average_price(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        
        # Get all category IDs including descendants
        def get_all_descendant_ids(category):
            """Recursively get all descendant category IDs"""
            descendant_ids = [category.id]
            for child in category.get_children():
                descendant_ids.extend(get_all_descendant_ids(child))
            return descendant_ids
        
        all_category_ids = get_all_descendant_ids(category)
        
        # Calculate average price for products in these categories
        avg_price = Product.objects.filter(
            category_id__in=all_category_ids
        ).aggregate(avg_price=Avg('price'))['avg_price'] or 0
        
        return Response({
            'category': category.name,
            'average_price': round(float(avg_price), 2)
        })
    
    except Category.DoesNotExist:
        return Response(
            {'error': 'Category not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
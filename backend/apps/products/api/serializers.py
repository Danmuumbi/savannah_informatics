from rest_framework import serializers
from apps.products.models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_children(self, obj):
        """Recursively get children categories"""
        children = obj.get_children()
        serializer = CategorySerializer(children, many=True)
        return serializer.data

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
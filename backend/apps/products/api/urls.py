from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/average-price/', views.category_average_price, name='category-average-price'),
]
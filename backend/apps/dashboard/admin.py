from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from apps.core.models import User
from apps.customers.models import Customer
from apps.products.models import Category, Product
from apps.orders.models import Order, OrderItem

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_customer', 'is_admin', 'is_staff')
    list_filter = ('is_customer', 'is_admin', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'is_customer', 'is_admin')}),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('created_at',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock', 'stock_quantity', 'created_at')
    list_filter = ('category', 'in_stock', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
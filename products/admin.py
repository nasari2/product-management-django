from django.contrib import admin
from .models import Category, Product, Sale

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'stock', 'is_active', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'sku')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'unit_price', 'customer_name', 'sold_at')
    list_filter = ('sold_at',)
    search_fields = ('product__name', 'customer_name')

from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.pk])

    @property
    def stock_status(self):
        if self.stock == 0: return 'Out of stock'
        if self.stock <= 5: return 'Low stock'
        return 'In stock'

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=150, blank=True)
    sold_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sold_at']

    @property
    def total(self):
        return self.quantity * self.unit_price

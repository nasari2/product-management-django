from django import forms
from .models import Category, Product, Sale

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','sku','category','description','price','stock','image','is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Product description'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['quantity','customer_name']
        widgets = {'quantity': forms.NumberInput(attrs={'min': 1}), 'customer_name': forms.TextInput(attrs={'placeholder': 'Optional'})}

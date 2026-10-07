from django.contrib import messages
from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm, CategoryForm, SaleForm
from .models import Product, Category, Sale

def dashboard(request):
    products = Product.objects.select_related('category')
    context = {
        'product_count': products.count(), 'category_count': Category.objects.count(),
        'stock_units': products.aggregate(total=Sum('stock'))['total'] or 0,
        'sales_count': Sale.objects.count(),
        'sales_total': Sale.objects.aggregate(total=Sum(ExpressionWrapper(F('quantity') * F('unit_price'), output_field=DecimalField(max_digits=12, decimal_places=2))))['total'] or 0,
        'low_stock': products.filter(stock__lte=5).order_by('stock')[:6],
        'recent_sales': Sale.objects.select_related('product')[:6],
    }
    return render(request, 'products/dashboard.html', context)

def product_list(request):
    products = Product.objects.select_related('category').all()
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    if q: products = products.filter(Q(name__icontains=q) | Q(sku__icontains=q) | Q(description__icontains=q))
    if category: products = products.filter(category_id=category)
    if status == 'low': products = products.filter(stock__lte=5, stock__gt=0)
    elif status == 'out': products = products.filter(stock=0)
    elif status == 'active': products = products.filter(is_active=True)
    return render(request, 'products/product_list.html', {'products': products, 'categories': Category.objects.all(), 'q': q, 'selected_category': category, 'status': status})

def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = form.save(); messages.success(request, f'{product.name} added successfully.'); return redirect('products:product_detail', product.pk)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add Product'})

def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    sales = product.sales.all()[:10]
    return render(request, 'products/product_detail.html', {'product': product, 'sales': sales, 'sale_form': SaleForm()})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save(); messages.success(request, 'Product updated successfully.'); return redirect('products:product_detail', product.pk)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name; product.delete(); messages.success(request, f'{name} deleted.'); return redirect('products:product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

def record_sale(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = SaleForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        qty = form.cleaned_data['quantity']
        if qty > product.stock:
            messages.error(request, f'Only {product.stock} units are available.')
        else:
            sale = form.save(commit=False); sale.product = product; sale.unit_price = product.price; sale.save()
            product.stock -= qty; product.save(update_fields=['stock','updated_at'])
            messages.success(request, 'Sale recorded and inventory updated.');
    return redirect('products:product_detail', product.pk)

def category_list(request):
    return render(request, 'products/category_list.html', {'categories': Category.objects.all()})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request, 'Category added.'); return redirect('products:category_list')
    return render(request, 'products/category_form.html', {'form': form, 'title': 'Add Category'})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk); form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid(): form.save(); messages.success(request, 'Category updated.'); return redirect('products:category_list')
    return render(request, 'products/category_form.html', {'form': form, 'title': 'Edit Category'})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try: category.delete(); messages.success(request, 'Category deleted.')
        except Exception: messages.error(request, 'Cannot delete a category that contains products.')
        return redirect('products:category_list')
    return render(request, 'products/category_confirm_delete.html', {'category': category})

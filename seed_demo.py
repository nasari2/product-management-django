import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','product_management.settings')
import django
django.setup()
from products.models import Category, Product

categories = ['Electronics','Office','Home & Kitchen','Accessories']
for name in categories: Category.objects.get_or_create(name=name)
items = [
('Wireless Mouse','ELEC-001','Electronics',799,24,'Ergonomic wireless mouse with USB receiver.'),
('Mechanical Keyboard','ELEC-002','Electronics',2499,8,'Compact mechanical keyboard for productivity.'),
('Notebook A5','OFF-001','Office',149,50,'Hard-cover A5 ruled notebook.'),
('Desk Lamp','HOME-001','Home & Kitchen',1199,4,'Adjustable LED desk lamp.'),
('Laptop Stand','ACC-001','Accessories',999,0,'Aluminium adjustable laptop stand.'),
]
for name,sku,cat,price,stock,desc in items:
    Product.objects.get_or_create(sku=sku, defaults={'name':name,'category':Category.objects.get(name=cat),'price':price,'stock':stock,'description':desc})
print('Demo data created.')

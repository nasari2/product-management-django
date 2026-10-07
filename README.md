# Mini Product Management Website — Django

A complete mini product-management web app built with Python and Django.

## Features
- Add, edit and delete products
- Product image upload
- Set product price and SKU
- Manage inventory/stock
- Low-stock and out-of-stock status
- Product search by name, SKU and description
- Filter by category and stock status
- Category CRUD
- Product detail page
- Record sales and automatically reduce stock
- Sales history per product
- Dashboard with product, category, stock and sales statistics
- Responsive UI
- SQLite database
- Django admin support

## Requirements
- Python 3.10+ recommended
- pip

## Windows setup
Open PowerShell in this project folder:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python seed_demo.py
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Admin
Create an admin user:
```powershell
python manage.py createsuperuser
```
Then open http://127.0.0.1:8000/admin/

## Submission checklist
1. Install dependencies.
2. Run migrations.
3. Run the demo seed script.
4. Test Add/Edit/Delete product.
5. Test image upload.
6. Test category management.
7. Test search/filter.
8. Open a product and record a sale to verify stock decreases.
9. Zip the complete project folder for submission.

## Main folders
- `product_management/` — Django project settings and URLs
- `products/` — models, forms, views, templates, CSS and migrations
- `media/` — uploaded product images
- `seed_demo.py` — optional demo data

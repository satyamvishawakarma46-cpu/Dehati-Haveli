# Dehati Haveli Restaurant Website

A Django + SQLite restaurant website with:
- Responsive home page
- Menu categories and items
- Session-based shopping cart
- Checkout/order form
- WhatsApp order button
- Django admin panel for menu and orders
- Simple login/signup pages
- SQLite database

## Run

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

The restaurant phone number is set to 9792197857 in `restaurant/views.py`.
Update the address in `templates/base.html` and `restaurant/views.py` as needed.

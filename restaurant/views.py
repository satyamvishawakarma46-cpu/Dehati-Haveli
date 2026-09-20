from urllib.parse import quote
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, MenuItem, Order, OrderItem

WHATSAPP_NUMBER = "91792197857"

def cart_items(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0")
    for item_id, qty in cart.items():
        item = MenuItem.objects.filter(id=item_id, available=True).first()
        if item:
            subtotal = item.price * qty
            items.append({"item": item, "qty": qty, "subtotal": subtotal})
            total += subtotal
    return items, total

def home(request):
    categories = Category.objects.prefetch_related("items").all()
    return render(request, "home.html", {"categories": categories})

def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id, available=True)
    cart = request.session.get("cart", {})
    key = str(item.id)
    cart[key] = cart.get(key, 0) + 1
    request.session["cart"] = cart
    messages.success(request, f"{item.name} cart me add ho gaya.")
    return redirect(request.META.get("HTTP_REFERER", "home"))

def remove_from_cart(request, item_id):
    cart = request.session.get("cart", {})
    key = str(item_id)
    if key in cart:
        del cart[key]
    request.session["cart"] = cart
    return redirect("cart")

def cart(request):
    items, total = cart_items(request)
    return render(request, "cart.html", {"items": items, "total": total})

def checkout(request):
    items, total = cart_items(request)
    if not items:
        messages.warning(request, "Cart empty hai.")
        return redirect("home")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        notes = request.POST.get("notes", "").strip()

        if not name or not phone or not address:
            messages.error(request, "Name, phone aur address required hain.")
            return render(request, "checkout.html", {"items": items, "total": total})

        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            name=name,
            phone=phone,
            address=address,
            notes=notes,
            total=total,
        )

        for row in items:
            OrderItem.objects.create(
                order=order,
                menu_item=row["item"],
                quantity=row["qty"],
                price=row["item"].price,
            )

        request.session["cart"] = {}

        lines = [
            f"Namaste Dehati Haveli, Order #{order.id}",
            f"Name: {name}",
            f"Phone: {phone}",
            f"Address: {address}",
            "Items:"
        ]
        for row in items:
            lines.append(f"- {row['item'].name} x {row['qty']} = ₹{row['subtotal']}")
        lines.append(f"Total: ₹{total}")
        if notes:
            lines.append(f"Note: {notes}")

        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(chr(10).join(lines))}"
        return render(request, "order_success.html", {
            "order": order,
            "whatsapp_url": whatsapp_url
        })

    return render(request, "checkout.html", {"items": items, "total": total})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_success.html", {"order": order, "whatsapp_url": None})

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if not username or not password:
            messages.error(request, "Username aur password required hain.")
            return render(request, "signup.html")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "signup.html")
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("home")
    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid username/password.")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

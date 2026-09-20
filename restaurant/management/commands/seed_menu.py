from django.core.management.base import BaseCommand
from restaurant.models import Category, MenuItem

MENU = {
    "Paratha": [
        ("Paneer Paratha", 100), ("Aloo Paratha", 60),
        ("Mix Paratha", 80), ("Pyaz Paratha", 70),
    ],
    "Paneer": [
        ("Matar Paneer", 160), ("Shahi Paneer", 200),
        ("Kadhai Paneer", 280), ("Handi Paneer", 280),
        ("Kaju Curry", 280), ("Kaju Paneer", 280),
        ("Khoya Paneer", 280), ("Paneer Masala", 260),
        ("Paneer Butter Masala", 260), ("Paneer Do Pyaza", 260),
    ],
    "Rice": [
        ("Plain Rice", 80), ("Jeera Rice", 110),
        ("Veg Fried Rice", 140), ("Paneer Fried Rice", 150),
        ("Veg Biryani", 120), ("Matar Pulao", 140),
        ("Paneer Pulao", 140), ("Matar Paneer Pulao", 160),
    ],
    "Sabji": [
        ("Mix Veg", 90), ("Aloo Jeera", 60), ("Aloo Matar Dry", 60),
        ("Aloo Matar Gravy", 60), ("Aloo Tomato", 60),
        ("Aloo Bhindi", 60), ("Dum Aloo", 140),
        ("Sev Bhaji", 150), ("Sev Tomato", 150),
        ("Stuff Dum Aloo", 160),
    ],
    "Roti": [
        ("Tandoor Roti Plain", 7), ("Tandoor Butter Roti", 10),
        ("Tawa Roti", 12), ("Tawa Butter Roti", 15),
        ("Missi Butter Roti", 30), ("Plain Naan", 35),
        ("Lachha Paratha", 35), ("Stuff Naan", 70),
        ("Garlic Naan", 70), ("Dhaniya Roti", 20),
    ],
    "Dal": [
        ("Matka Dal", 180), ("Dal Fry", 100),
        ("Dal Fry Butter", 120), ("Dal Tadka", 120),
        ("Dal Makhani", 160),
    ],
    "Raita": [
        ("Dahi Raita", 90), ("Boondi Raita", 90),
        ("Mix Raita", 120), ("Veg Raita", 120), ("Fruits Raita", 180),
    ],
    "Mansharam": [
        ("Mansharam Masala", 260), ("Kadhai Mansharam", 260),
        ("Paneer Mansharam", 280), ("Malai Kofta", 280),
    ],
    "Snacks (Nasta)": [
        ("Paneer Pakodi", 140), ("Mix Pakodi", 100),
        ("Pyaz Pakodi", 100), ("Aloo Pakodi", 100),
        ("Peanut Masala", 120), ("Papad Masala", 50),
        ("Papad Roasted", 15), ("Papad Fry", 25), ("Matar Fry", 120),
    ],
    "Special Snacks": [
        ("Plain Maggi", 70), ("Maggi Masala", 80),
        ("Veg Maggi", 90), ("Veg Manchurian", 120),
        ("Paneer Manchurian", 140),
    ],
    "Sweets": [
        ("Kheer", 60), ("Chhena", 30), ("Gulab Jamun", 25), ("Ras Malai", 50),
    ],
}

class Command(BaseCommand):
    help = "Populate Dehati Haveli menu"

    def handle(self, *args, **kwargs):
        for order, (cat_name, items) in enumerate(MENU.items()):
            cat, _ = Category.objects.get_or_create(name=cat_name, defaults={"order": order})
            cat.order = order
            cat.save()
            for name, price in items:
                MenuItem.objects.get_or_create(
                    category=cat, name=name,
                    defaults={"price": price, "description": "Dehati Haveli special"}
                )
        self.stdout.write(self.style.SUCCESS("Menu seeded successfully."))

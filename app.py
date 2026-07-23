from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Fresh Milk", "price": 45, "category": "Essentials", "desc": "Toned milk, 1 litre", "badge": "Popular"},
    {"id": 2, "name": "Bread", "price": 35, "category": "Bakery", "desc": "Soft whole wheat loaf", "badge": "Fresh"},
    {"id": 3, "name": "Bananas", "price": 40, "category": "Fruits", "desc": "Fresh yellow bananas", "badge": "Top pick"},
    {"id": 4, "name": "Eggs", "price": 60, "category": "Essentials", "desc": "Pack of 6", "badge": "Best seller"},
    {"id": 5, "name": "Orange Juice", "price": 95, "category": "Drinks", "desc": "Cold pressed, 1 litre", "badge": "New"},
    {"id": 6, "name": "Chips", "price": 30, "category": "Snacks", "desc": "Crunchy salted chips", "badge": "Hot"},
    {"id": 7, "name": "Greek Yogurt", "price": 120, "category": "Dairy", "desc": "Creamy snack cup", "badge": "Healthy"},
    {"id": 8, "name": "Tomatoes", "price": 55, "category": "Vegetables", "desc": "Juicy farm tomatoes", "badge": "Seasonal"},
    {"id": 9, "name": "Spinach", "price": 42, "category": "Vegetables", "desc": "Fresh leafy greens", "badge": "Daily"},
    {"id": 10, "name": "Chicken Breast", "price": 220, "category": "Meat", "desc": "Boneless tender cuts", "badge": "Protein"},
    {"id": 11, "name": "Salmon Fillet", "price": 320, "category": "Seafood", "desc": "Premium sliced fish", "badge": "Chef pick"},
    {"id": 12, "name": "Rice", "price": 90, "category": "Pantry", "desc": "Basmati rice, 1 kg", "badge": "Staple"},
    {"id": 13, "name": "Pasta", "price": 70, "category": "Pantry", "desc": "Italian durum pasta", "badge": "Comfort"},
    {"id": 14, "name": "Olive Oil", "price": 180, "category": "Pantry", "desc": "Extra virgin cooking oil", "badge": "Premium"},
    {"id": 15, "name": "Honey", "price": 140, "category": "Pantry", "desc": "Natural wildflower honey", "badge": "Sweet"},
    {"id": 16, "name": "Cereal", "price": 150, "category": "Breakfast", "desc": "Crunchy breakfast blend", "badge": "Morning"},
    {"id": 17, "name": "Coffee", "price": 210, "category": "Breakfast", "desc": "Ground coffee beans", "badge": "Aroma"},
    {"id": 18, "name": "Apples", "price": 85, "category": "Fruits", "desc": "Crisp red apples", "badge": "Fresh"},
    {"id": 19, "name": "Avocados", "price": 95, "category": "Fruits", "desc": "Creamy ripe avocados", "badge": "Trend"},
    {"id": 20, "name": "Soda", "price": 55, "category": "Drinks", "desc": "Sparkling citrus soda", "badge": "Cool"},
    {"id": 21, "name": "Water Bottles", "price": 70, "category": "Drinks", "desc": "Pack of 6 purified bottles", "badge": "Hydrate"},
    {"id": 22, "name": "Trail Mix", "price": 110, "category": "Snacks", "desc": "Nutty energy snack", "badge": "Crunch"},
    {"id": 23, "name": "Cookies", "price": 75, "category": "Snacks", "desc": "Butter cookies", "badge": "Treat"},
    {"id": 24, "name": "Dish Soap", "price": 90, "category": "Household", "desc": "Citrus cleaning liquid", "badge": "Clean"},
]

orders = []


@app.route("/")
def home():
    return render_template("index.html", title="QuickCart Delivery")


@app.route("/about")
def about():
    return render_template("about.html", title="About QuickCart")


@app.route("/services")
def services():
    return render_template("services.html", title="QuickCart Services")


@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact QuickCart")


@app.route("/api/products")
def api_products():
    categories = sorted({product["category"] for product in products})
    return jsonify({"products": products, "categories": categories})


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "orders": len(orders)})


@app.route("/api/order", methods=["POST"])
def place_order():
    payload = request.get_json(silent=True) or {}
    items = payload.get("items", [])
    customer = payload.get("customer", {})

    if not items:
        return jsonify({"ok": False, "message": "Please add at least one item to your cart."}), 400

    selected = []
    total = 0
    for item in items:
        product = next((p for p in products if p["id"] == item["id"]), None)
        if product:
            quantity = max(1, int(item.get("quantity", 1)))
            price = product["price"] * quantity
            total += price
            selected.append({
                "id": product["id"],
                "name": product["name"],
                "quantity": quantity,
                "price": price,
            })

    order = {
        "id": len(orders) + 1,
        "customer": customer,
        "items": selected,
        "total": round(total, 2),
        "status": "Confirmed",
        "eta": "18-25 min",
        "delivery_window": "Today, 6:00 PM - 8:00 PM",
        "payment": "Card on delivery",
    }
    orders.append(order)

    return jsonify({
        "ok": True,
        "message": f"Order #{order['id']} placed successfully!",
        "order": order,
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

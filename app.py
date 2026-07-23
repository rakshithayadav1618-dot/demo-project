from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Fresh Milk", "price": 45, "category": "Essentials", "desc": "Toned milk, 1 litre", "badge": "Popular"},
    {"id": 2, "name": "Bread", "price": 35, "category": "Bakery", "desc": "Soft whole wheat loaf", "badge": "Fresh"},
    {"id": 3, "name": "Bananas", "price": 40, "category": "Fruits", "desc": "Fresh yellow bananas", "badge": "Top pick"},
    {"id": 4, "name": "Eggs", "price": 60, "category": "Essentials", "desc": "Pack of 6", "badge": "Best seller"},
    {"id": 5, "name": "Orange Juice", "price": 95, "category": "Drinks", "desc": "Cold pressed, 1 litre", "badge": "New"},
    {"id": 6, "name": "Chips", "price": 30, "category": "Snacks", "desc": "Crunchy salted chips", "badge": "Hot"},
]

orders = []


@app.route("/")
def home():
    return render_template("index.html")


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
    }
    orders.append(order)

    return jsonify({
        "ok": True,
        "message": f"Order #{order['id']} placed successfully!",
        "order": order,
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


from flask import Flask, request, jsonify
from external_api import search_by_barcode, search_by_name

app = Flask(__name__)


inventory = [
    {
        "id": 1,
        "name": "Milk",
        "category": "Dairy",
        "quantity": 20,
        "price": 65.00,
        "barcode": "6161101234567"
    },
    {
        "id": 2,
        "name": "Bread",
        "category": "Bakery",
        "quantity": 15,
        "price": 60.00,
        "barcode": "6161101234668"
    },
    {
        "id": 3,
        "name": "Rice",
        "category": "Grains",
        "quantity": 30,
        "price": 180.00,
        "barcode": "6161101234579"
    }
]

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Inventory Management API"
    }), 200


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


@app.route("/inventory/<int:product_id>", methods=["GET"])
def get_product(product_id):

    for product in inventory:
        if product["id"] == product_id:
            return jsonify(product), 200

    return jsonify({"error": "Product not found"}), 404


@app.route("/inventory", methods=["POST"])
def add_product():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please provide product details as JSON"
        }), 400

    required_fields = ["name", "category", "quantity", "price"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({"error": "Invalid product name"}), 400

    if not isinstance(data["category"], str) or not data["category"].strip():
        return jsonify({"error": "Invalid product category"}), 400

    if type(data["quantity"]) is not int or data["quantity"] < 0:
        return jsonify({"error": "Quantity must be a non-negative whole number"}), 400

    if (
        isinstance(data["price"], bool)
        or not isinstance(data["price"], (int, float))
        or data["price"] < 0
    ):
        return jsonify({"error": "Price must be a non-negative number"}), 400

    new_id = max(
        (product["id"] for product in inventory),
        default=0
    ) + 1

    new_product = {
        "id": new_id,
        "name": data["name"].strip(),
        "category": data["category"].strip(),
        "quantity": data["quantity"],
        "price": float(data["price"]),
        "barcode": data.get("barcode", "")
    }

    inventory.append(new_product)

    return jsonify({
        "message": "Product added successfully",
        "product": new_product
    }), 201


@app.route("/inventory/<int:product_id>", methods=["PATCH"])
def update_product(product_id):

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Please provide product details to update"
        }), 400

    for product in inventory:

        if product["id"] == product_id:

            allowed_fields = [
                "name", "category", "quantity", "price", "barcode"
            ]

            for field, value in data.items():

                if field not in allowed_fields:
                    return jsonify({
                        "error": f"Cannot update field: {field}"
                    }), 400

                if field in ["name", "category"]:
                    if not isinstance(value, str) or not value.strip():
                        return jsonify({
                            "error": f"{field} must be a non-empty string"
                        }), 400

                if field == "quantity":
                    if type(value) is not int or value < 0:
                        return jsonify({
                            "error": "Quantity must be a non-negative whole number"
                        }), 400

                if field == "price":
                    if (
                        isinstance(value, bool)
                        or not isinstance(value, (int, float))
                        or value < 0
                    ):
                        return jsonify({
                            "error": "Price must be a non-negative number"
                        }), 400

                if field == "barcode" and not isinstance(value, str):
                    return jsonify({
                        "error": "Barcode must be a string"
                    }), 400

            for field, value in data.items():

                if field in ["name", "category"]:
                    value = value.strip()

                if field == "price":
                    value = float(value)

                product[field] = value

            return jsonify({
                "message": "Product updated successfully",
                "product": product
            }), 200

    return jsonify({"error": "Product not found"}), 404


@app.route("/inventory/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    for product in inventory:

        if product["id"] == product_id:

            inventory.remove(product)

            return jsonify({
                "message": "Product deleted successfully"
            }), 200

    return jsonify({"error": "Product not found"}), 404


@app.route("/search/barcode/<barcode>", methods=["GET"])
def search_barcode(barcode):

    product = search_by_barcode(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found or external service unavailable"
        }), 404

    return jsonify(product), 200


@app.route("/search/name/<name>", methods=["GET"])
def search_name(name):

    product = search_by_name(name)

    if product is None:
        return jsonify({
            "error": "Product not found or external service unavailable"
        }), 404

    return jsonify(product), 200


@app.route("/inventory/from-api/<barcode>", methods=["POST"])
def add_product_from_api(barcode):

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please provide quantity and price as JSON"
        }), 400

    if "quantity" not in data or "price" not in data:
        return jsonify({
            "error": "Quantity and price are required"
        }), 400

    quantity = data["quantity"]
    price = data["price"]

    if type(quantity) is not int or quantity < 0:
        return jsonify({
            "error": "Quantity must be a non-negative whole number"
        }), 400

    if (
        isinstance(price, bool)
        or not isinstance(price, (int, float))
        or price < 0
    ):
        return jsonify({
            "error": "Price must be a non-negative number"
        }), 400

    
    for product in inventory:

        if product["barcode"] == barcode:
            return jsonify({
                "error": "Product already exists in inventory"
            }), 409


    external_product = search_by_barcode(barcode)

    if external_product is None:
        return jsonify({
            "error": "Product not found or external service unavailable"
        }), 404

    product_name = (
        external_product.get("product_name")
        or external_product.get("product_name_en")
    )

    if not product_name:
        return jsonify({
            "error": "External product does not have a name"
        }), 404

    categories = external_product.get("categories", "")

    category = (
        categories.split(",")[0].strip()
        if categories
        else "Uncategorized"
    )

    new_id = max(
        (product["id"] for product in inventory),
        default=0
    ) + 1

    new_product = {
        "id": new_id,
        "name": product_name,
        "category": category,
        "quantity": quantity,
        "price": float(price),
        "barcode": barcode
    }

    inventory.append(new_product)

    return jsonify({
        "message": "External product added successfully",
        "product": new_product
    }), 201


if __name__ == "__main__":
    app.run(debug=True)




import requests

BASE_URL = "http://127.0.0.1:5000"


def show_inventory():
    """Display all products in the inventory."""

    try:
        response = requests.get(f"{BASE_URL}/inventory", timeout=10)

        if response.status_code == 200:
            products = response.json()

            if not products:
                print("\nYour inventory is empty.")
                return

            print("\n========== INVENTORY ==========")

            for product in products:
                print(f"""
ID:       {product['id']}
Name:     {product['name']}
Category: {product['category']}
Quantity: {product['quantity']}
Price:    {product['price']}
Barcode:  {product.get('barcode', '')}
""")
        else:
            print("Could not retrieve inventory.")

    except requests.RequestException:
        print("Cannot connect to the API. Please start the Flask server.")


def add_product():
    """Add a product manually."""

    print("\n========== ADD PRODUCT ==========")

    try:
        name = input("Product name: ").strip()
        category = input("Category: ").strip()
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))
        barcode = input("Barcode (optional): ").strip()

        product = {
            "name": name,
            "category": category,
            "quantity": quantity,
            "price": price,
            "barcode": barcode
        }

        response = requests.post(
            f"{BASE_URL}/inventory",
            json=product,
            timeout=10
        )

        print(response.json())

    except ValueError:
        print("Please enter a valid number for quantity and price.")

    except requests.RequestException:
        print("Cannot connect to the API. Please start the Flask server.")


def find_product():
    """Find a product using its inventory ID."""

    try:
        product_id = int(input("\nEnter product ID: "))

        response = requests.get(
            f"{BASE_URL}/inventory/{product_id}",
            timeout=10
        )

        print("\n", response.json())

    except ValueError:
        print("Please enter a valid product ID.")

    except requests.RequestException:
        print("Cannot connect to the API.")


def update_product():
    """Update an existing product."""

    try:
        product_id = int(input("\nEnter product ID to update: "))

        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Category")
        print("3. Quantity")
        print("4. Price")
        print("5. Barcode")

        choice = input("Choose an option: ")

        if choice == "1":
            updates = {"name": input("Enter new name: ").strip()}

        elif choice == "2":
            updates = {"category": input("Enter new category: ").strip()}

        elif choice == "3":
            updates = {"quantity": int(input("Enter new quantity: "))}

        elif choice == "4":
            updates = {"price": float(input("Enter new price: "))}

        elif choice == "5":
            updates = {"barcode": input("Enter new barcode: ").strip()}

        else:
            print("Invalid choice.")
            return

        response = requests.patch(
            f"{BASE_URL}/inventory/{product_id}",
            json=updates,
            timeout=10
        )

        print(response.json())

    except ValueError:
        print("Please enter a valid number.")

    except requests.RequestException:
        print("Cannot connect to the API.")


def delete_product():
    """Delete a product from the inventory."""

    try:
        product_id = int(input("\nEnter product ID to delete: "))

        confirm = input("Are you sure you want to delete it? (y/n): ")

        if confirm.lower() != "y":
            print("Deletion cancelled.")
            return

        response = requests.delete(
            f"{BASE_URL}/inventory/{product_id}",
            timeout=10
        )

        print(response.json())

    except ValueError:
        print("Please enter a valid product ID.")

    except requests.RequestException:
        print("Cannot connect to the API.")


def search_external_product():
    """Search OpenFoodFacts by barcode or name."""

    print("\n1. Search by barcode")
    print("2. Search by product name")

    choice = input("Choose an option: ")

    if choice == "1":
        barcode = input("Enter barcode: ").strip()
        url = f"{BASE_URL}/search/barcode/{barcode}"

    elif choice == "2":
        name = input("Enter product name: ").strip()
        url = f"{BASE_URL}/search/name/{name}"

    else:
        print("Invalid choice.")
        return

    try:
        response = requests.get(url, timeout=20)
        print("\nExternal API response:")
        print(response.json())

    except requests.RequestException:
        print("Could not connect to the API.")


def add_external_product():
    """Fetch an external product and save it to inventory."""

    barcode = input("\nEnter product barcode: ").strip()

    try:
        quantity = int(input("Enter quantity to stock: "))
        price = float(input("Enter your selling price: "))

        response = requests.post(
            f"{BASE_URL}/inventory/from-api/{barcode}",
            json={
                "quantity": quantity,
                "price": price
            },
            timeout=20
        )

        print("\n", response.json())

    except ValueError:
        print("Please enter valid numbers.")

    except requests.RequestException:
        print("Could not connect to the API.")


def main():
    """Display the CLI menu."""

    while True:
        print("\n================================")
        print("   INVENTORY MANAGEMENT SYSTEM")
        print("================================")
        print("1. View all products")
        print("2. Add a product")
        print("3. Find a product by ID")
        print("4. Update a product")
        print("5. Delete a product")
        print("6. Search OpenFoodFacts")
        print("7. Add product from OpenFoodFacts")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            show_inventory()

        elif choice == "2":
            add_product()

        elif choice == "3":
            find_product()

        elif choice == "4":
            update_product()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            search_external_product()

        elif choice == "7":
            add_external_product()

        elif choice == "8":
            print("Thank you for using the Inventory Management System!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

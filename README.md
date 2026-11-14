# Inventory Management System

## 1. Project Description

The Inventory Management System is a Python application developed using Flask. It allows users to manage products through a REST API and a command-line interface.

The system supports adding, viewing, updating and deleting products. It also connects to the OpenFoodFacts API to search for product information using a barcode or product name.

## 2. Features

- Add new products to the inventory.
- View all available products.
- Search for a product using its ID.
- Update product information.
- Delete products from the inventory.
- Search OpenFoodFacts using a barcode.
- Search OpenFoodFacts using a product name.
- Fetch product details from OpenFoodFacts and add the product to the inventory.
- Manage inventory through a command-line interface.
- Run automated tests using pytest.

## 3. Technologies Used

- Python
- Flask
- Requests
- Pytest
- Git and GitHub

## 4. Project Structure

text
inventory-management-system/
│
├── app.py
├── cli.py
├── external_api.py
├── requirements.txt
├── README.md
│
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_cli.py
    └── test_external_api.py
```

## 5. Installation and Setup


 Create a virtual environment

```bash
python3 -m venv venv
```

 Activate the virtual environment

```bash
source venv/bin/activate
```

 Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Running the Application

Start the Flask server:

```bash
python -m flask --app app run
```


## 7. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Display the welcome message |
| GET | /inventory | View all products |
| GET | /inventory/{id} | View one product |
| POST | /inventory | Add a product |
| PATCH | /inventory/{id} | Update a product |
| DELETE | /inventory/{id} | Delete a product |
| GET | /search/barcode/{barcode} | Search OpenFoodFacts by barcode |
| GET | /search/name/{name} | Search OpenFoodFacts by name |
| POST | /inventory/from-api/{barcode} | Fetch an external product and add it to inventory |

### Example: Add a product

Send a POST request to:

```text
http://127.0.0.1:5000/inventory
```

Example JSON:

```json
{
    "name": "Sugar",
    "category": "Grocery",
    "quantity": 10,
    "price": 150,
    "barcode": "123456789"
}
```

### Example: Update a product

Send a PATCH request to:

```text
http://127.0.0.1:5000/inventory/1
```

Example JSON:

```json
{
    "price": 80,
    "quantity": 25
}
```




The application retrieves the product details from OpenFoodFacts and uses the supplied quantity and selling price when adding it to inventory.

## 8. Running the Command-Line Interface

Keep the Flask server running in one terminal.

Open another terminal, activate the virtual environment and run:

```bash
python cli.py
```

The CLI provides these options:

1. View all products
2. Add a product
3. Find a product by ID
4. Update a product
5. Delete a product
6. Search OpenFoodFacts
7. Add a product from OpenFoodFacts
8. Exit

## 9. Running the Tests

The project uses pytest to test the API, CLI and external API functions.

Install pytest if necessary:

```bash
pip install pytest
```

Run all tests:

```bash
python -m pytest -v
```

The tests use mocked responses to test external API operations without depending on the availability of the live OpenFoodFacts service.

## 10. External API Integration

The application uses the OpenFoodFacts API to retrieve product information.

It supports:

- Searching for products using barcodes.
- Searching for products using product names.
- Retrieving product names and categories.
- Adding retrieved product details to the local inventory.


## 11. Data Storage

The current application stores inventory products in a Python list while the Flask application is running. The sample products are loaded when the application starts.


## 12. Author

Developed as a Python Flask REST API and Inventory Management System project.

import copy
import app as app_module
import pytest


@pytest.fixture
def client():
    """Create a test client and reset the inventory before each test."""

    original_inventory = copy.deepcopy(app_module.inventory)

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        app_module.inventory[:] = copy.deepcopy(original_inventory)
        yield test_client

    app_module.inventory[:] = original_inventory


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Welcome" in response.get_json()["message"]


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_get_one_product(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Milk"


def test_get_missing_product(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404


def test_add_product(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Sugar",
            "category": "Grocery",
            "quantity": 10,
            "price": 150
        }
    )

    assert response.status_code == 201
    assert response.get_json()["product"]["name"] == "Sugar"


def test_add_product_missing_field(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Sugar",
            "quantity": 10,
            "price": 150
        }
    )

    assert response.status_code == 400


def test_update_product(client):
    response = client.patch(
        "/inventory/1",
        json={"price": 80}
    )

    assert response.status_code == 200
    assert response.get_json()["product"]["price"] == 80.0


def test_update_missing_product(client):
    response = client.patch(
        "/inventory/999",
        json={"price": 80}
    )

    assert response.status_code == 404


def test_delete_product(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200

    remaining = client.get("/inventory").get_json()

    assert len(remaining) == 2


def test_delete_missing_product(client):
    response = client.delete("/inventory/999")

    assert response.status_code == 404


def test_search_barcode(client, monkeypatch):
    fake_product = {
        "product_name": "Nutella",
        "categories": "Hazelnut spreads"
    }

    monkeypatch.setattr(
        app_module,
        "search_by_barcode",
        lambda barcode: fake_product
    )

    response = client.get("/search/barcode/3017620422003")

    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Nutella"


def test_search_name(client, monkeypatch):
    fake_product = {"product_name": "Nutella"}

    monkeypatch.setattr(
        app_module,
        "search_by_name",
        lambda name: fake_product
    )

    response = client.get("/search/name/Nutella")

    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Nutella"


def test_add_product_from_api(client, monkeypatch):
    fake_product = {
        "product_name": "Nutella",
        "categories": "Hazelnut spreads"
    }

    monkeypatch.setattr(
        app_module,
        "search_by_barcode",
        lambda barcode: fake_product
    )

    response = client.post(
        "/inventory/from-api/3017620422003",
        json={"quantity": 10, "price": 500}
    )

    assert response.status_code == 201
    assert response.get_json()["product"]["name"] == "Nutella"


def test_add_product_from_api_missing_details(client):
    response = client.post(
        "/inventory/from-api/3017620422003",
        json={"quantity": 10}
    )

    assert response.status_code == 400

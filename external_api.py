
import requests
import time

BASE_URL = "https://world.openfoodfacts.org"

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0"
}


def search_by_barcode(barcode):
    """Search for a product using its barcode."""

    url = f"{BASE_URL}/api/v2/product/{barcode}.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        if data.get("status") == 1:
            return data.get("product")

        return None

    except (requests.RequestException, ValueError):
        return None


def search_by_name(name):
    """Search for a product using its name."""

    url = f"{BASE_URL}/cgi/search.pl"

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5
    }

    for attempt in range(3):
        try:
            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=15
            )

            if response.status_code == 503:
                time.sleep(2)
                continue

            response.raise_for_status()
            data = response.json()

            products = data.get("products", [])

            if products:
                return products[0]

            return None

        except (requests.RequestException, ValueError):
            return None

    return None





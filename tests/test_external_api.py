
import requests
import external_api


class FakeResponse:
    """A simple fake response for testing API requests."""

    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("Request failed")


def test_search_by_barcode_success(monkeypatch):
    fake_data = {
        "status": 1,
        "product": {"product_name": "Nutella"}
    }

    monkeypatch.setattr(
        external_api.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_data)
    )

    result = external_api.search_by_barcode("3017620422003")

    assert result["product_name"] == "Nutella"


def test_search_by_barcode_not_found(monkeypatch):
    fake_data = {"status": 0}

    monkeypatch.setattr(
        external_api.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_data)
    )

    result = external_api.search_by_barcode("0000000000000")

    assert result is None


def test_search_by_barcode_connection_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.ConnectionError("Connection failed")

    monkeypatch.setattr(
        external_api.requests,
        "get",
        fake_get
    )

    result = external_api.search_by_barcode("3017620422003")

    assert result is None


def test_search_by_name_success(monkeypatch):
    fake_data = {
        "products": [
            {"product_name": "Nutella"}
        ]
    }

    monkeypatch.setattr(
        external_api.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_data)
    )

    result = external_api.search_by_name("Nutella")

    assert result["product_name"] == "Nutella"


def test_search_by_name_not_found(monkeypatch):
    fake_data = {"products": []}

    monkeypatch.setattr(
        external_api.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_data)
    )

    result = external_api.search_by_name("Unknown product")

    assert result is None


def test_search_by_name_connection_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.ConnectionError("Connection failed")

    monkeypatch.setattr(
        external_api.requests,
        "get",
        fake_get
    )

    result = external_api.search_by_name("Nutella")

    assert result is None


def test_search_by_name_service_unavailable(monkeypatch):
    monkeypatch.setattr(
        external_api.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(
            {},
            status_code=503
        )
    )

    monkeypatch.setattr(
        external_api.time,
        "sleep",
        lambda seconds: None
    )

    result = external_api.search_by_name("Nutella")

    assert result is None

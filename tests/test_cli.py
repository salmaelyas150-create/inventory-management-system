
import cli


class FakeResponse:
    """Fake response returned by the API during CLI tests."""

    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data


def test_show_inventory(monkeypatch, capsys):
    fake_products = [
        {
            "id": 1,
            "name": "Milk",
            "category": "Dairy",
            "quantity": 20,
            "price": 65.0,
            "barcode": "12345"
        }
    ]

    monkeypatch.setattr(
        cli.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(fake_products)
    )

    cli.show_inventory()

    output = capsys.readouterr().out

    assert "Milk" in output


def test_add_product(monkeypatch):
    answers = iter([
        "Sugar",
        "Grocery",
        "10",
        "150",
        "12345"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(answers)
    )

    captured = {}

    def fake_post(url, json, timeout):
        captured["product"] = json
        return FakeResponse({"message": "Product added successfully"}, 201)

    monkeypatch.setattr(cli.requests, "post", fake_post)

    cli.add_product()

    assert captured["product"]["name"] == "Sugar"
    assert captured["product"]["quantity"] == 10


def test_find_product(monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": "1"
    )

    monkeypatch.setattr(
        cli.requests,
        "get",
        lambda *args, **kwargs: FakeResponse({"name": "Milk"})
    )

    cli.find_product()

    output = capsys.readouterr().out

    assert "Milk" in output


def test_update_product(monkeypatch):
    answers = iter(["1", "4", "100"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(answers)
    )

    captured = {}

    def fake_patch(url, json, timeout):
        captured["updates"] = json
        return FakeResponse({"message": "Product updated successfully"})

    monkeypatch.setattr(cli.requests, "patch", fake_patch)

    cli.update_product()

    assert captured["updates"]["price"] == 100.0


def test_delete_product(monkeypatch):
    answers = iter(["1", "y"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(answers)
    )

    captured = {}

    def fake_delete(url, timeout):
        captured["url"] = url
        return FakeResponse({"message": "Product deleted successfully"})

    monkeypatch.setattr(cli.requests, "delete", fake_delete)

    cli.delete_product()

    assert "/inventory/1" in captured["url"]


def test_search_external_product(monkeypatch, capsys):
    answers = iter(["1", "3017620422003"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(answers)
    )

    monkeypatch.setattr(
        cli.requests,
        "get",
        lambda *args, **kwargs: FakeResponse({
            "product_name": "Nutella"
        })
    )

    cli.search_external_product()

    output = capsys.readouterr().out

    assert "Nutella" in output


def test_add_external_product(monkeypatch, capsys):
    answers = iter(["3017620422003", "10", "500"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(answers)
    )

    captured = {}

    def fake_post(url, json, timeout):
        captured["url"] = url
        captured["data"] = json
        return FakeResponse({
            "message": "External product added successfully"
        }, 201)

    monkeypatch.setattr(cli.requests, "post", fake_post)

    cli.add_external_product()

    assert "3017620422003" in captured["url"]
    assert captured["data"]["quantity"] == 10
    assert captured["data"]["price"] == 500.0


def test_main_exit(monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": "8"
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Thank you" in output

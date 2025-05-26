import pytest
from src.models.product import Product


def test_apply_discount():
    prod = Product(1, "Auriculares", 1000.0, 2, "Gamer", "2023-01-01", "Sí", "No", 30)

    prod.apply_discount(10)

    assert prod.price == 900.0


def test_set_negative_price():
    prod = Product(1, "Auriculares", 1000.0, 2, "Gamer", "2023-01-01", "Sí", "No", 30)

    with pytest.raises(ValueError, match="Price cannot be negative"):
        prod.price = -100.0

from decimal import Decimal

import pytest

from apps.orders.exceptions import (
    PromoCodeNotFoundError,
)
from apps.orders.services import OrderService


@pytest.mark.django_db
def test_additional_ordering_information(valid_promo_code):
    """Тест расчета финальной суммы с промокодом."""
    service = OrderService()
    promo, final_amount = service.additional_ordering_information(
        Decimal("100.00"), "VALID", 1
    )

    assert promo.code == "VALID"
    assert final_amount == Decimal("90.00")


@pytest.mark.django_db
def test_create_order_success(user):
    service = OrderService()
    order = service.create_order(user.id, Decimal("100.00"), None)

    assert order.user_id == user.id
    assert order.amount == Decimal("100.00")
    assert order.final_amount == Decimal("100.00")
    assert order.promo_code is None


@pytest.mark.django_db
def test_create_order_with_promo(user, valid_promo_code):
    service = OrderService()
    order = service.create_order(user.id, Decimal("100.00"), "VALID")

    assert order.user_id == user.id
    assert order.amount == Decimal("100.00")
    assert order.final_amount == Decimal("90.00")
    assert order.promo_code.code == "VALID"

    from apps.orders.models import PromoCodeUsage

    assert PromoCodeUsage.objects.filter(
        user=user, promo_code=valid_promo_code
    ).exists()

    valid_promo_code.refresh_from_db()
    assert valid_promo_code.current_uses == 1


@pytest.mark.django_db
def test_create_order_with_invalid_promo(user):
    service = OrderService()

    with pytest.raises(PromoCodeNotFoundError):
        service.create_order(user.id, Decimal("100.00"), "INVALID")

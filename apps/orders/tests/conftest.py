from decimal import Decimal

import pytest
from django.utils import timezone

from apps.orders.models import Order, PromoCode, PromoCodeUsage, User


@pytest.fixture
def user(db):
    """Создает тестового пользователя."""
    return User.objects.create(username="testuser")


@pytest.fixture
def valid_promo_code(db):
    """Создает валидный промокод (активный, не исчерпанный)."""
    promo = PromoCode(
        code="VALID",
        discount_percent=Decimal("10.00"),
        date_from=timezone.now() - timezone.timedelta(days=1),
        date_until=timezone.now() + timezone.timedelta(days=1),
        max_uses=5,
        current_uses=0,
    )
    promo.save()
    return promo


@pytest.fixture
def expired_promo_code(db):
    """Создает просроченный промокод."""
    promo = PromoCode(
        code="EXPIRED",
        discount_percent=Decimal("10.00"),
        date_from=timezone.now() - timezone.timedelta(days=2),
        date_until=timezone.now() - timezone.timedelta(days=1),
        max_uses=5,
        current_uses=0,
    )
    promo.save()
    return promo


@pytest.fixture
def not_started_promo_code(db):
    """Создает еще не начавшийся промокод."""
    promo = PromoCode(
        code="NOTSTARTED",
        discount_percent=Decimal("10.00"),
        date_from=timezone.now() + timezone.timedelta(days=1),
        date_until=timezone.now() + timezone.timedelta(days=2),
        max_uses=5,
        current_uses=0,
    )
    promo.save()
    return promo


@pytest.fixture
def exhausted_promo_code(db):
    """Создает исчерпанный промокод (достигнут max_uses)."""
    promo = PromoCode(
        code="EXHAUSTED",
        discount_percent=Decimal("10.00"),
        date_from=timezone.now() - timezone.timedelta(days=1),
        date_until=timezone.now() + timezone.timedelta(days=1),
        max_uses=5,
        current_uses=5,
    )
    promo.save()
    return promo


@pytest.fixture
def used_promo_code(db, user):
    """Создает промокод с использованием от конкретного пользователя."""
    promo = PromoCode(
        code="VALID_USED",
        discount_percent=Decimal("10.00"),
        date_from=timezone.now() - timezone.timedelta(days=1),
        date_until=timezone.now() + timezone.timedelta(days=1),
        max_uses=5,
        current_uses=0,
    )
    promo.save()

    # Создаем заказ и использование промокода
    order = Order.objects.create(
        user=user,
        amount=Decimal("100.00"),
        final_amount=Decimal("90.00"),
        promo_code=promo,
    )
    PromoCodeUsage.objects.create(
        promo_code=promo,
        user=user,
        order=order,
    )
    return promo


@pytest.fixture
def order_viewset():
    """Создает экземпляр OrderViewSet с OrderService."""

    from apps.orders.services import OrderService
    from apps.orders.views import OrderViewSet

    service = OrderService()
    viewset = OrderViewSet(order_service=service)
    return viewset


@pytest.fixture
def api_factory():
    """Возвращает фабрику для создания API-запросов."""
    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()

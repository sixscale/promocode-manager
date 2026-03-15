import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.orders.services import OrderService


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_order_success(api_client, user, valid_promo_code):
    response = api_client.post(
        "/api/orders/",
        {"user_id": user.id, "amount": "100.00", "promo_code": "VALID"},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"] is True
    assert "id" in response.data["data"]
    assert response.data["data"]["user_id"] == user.id
    assert "final_amount" in response.data["data"]
    assert response.data["data"]["promo_code_details"]["code"] == "VALID"


@pytest.mark.django_db
def test_create_order_without_promo(api_client, user):
    response = api_client.post(
        "/api/orders/", {"user_id": user.id, "amount": "100.00"}, format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"] is True
    assert response.data["data"]["user_id"] == user.id


@pytest.mark.django_db
def test_create_order_invalid_promo(api_client, user):
    response = api_client.post(
        "/api/orders/",
        {"user_id": user.id, "amount": "100.00", "promo_code": "INVALID"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["success"] is False
    assert response.data["error"] == "PROMO_CODE_ERROR"


@pytest.mark.django_db
def test_create_order_user_not_found(api_client):
    response = api_client.post(
        "/api/orders/", {"user_id": 999, "amount": "100.00"}, format="json"
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data["success"] is False


@pytest.mark.django_db
def test_create_order_internal_error(api_client, user, monkeypatch):

    def mock_create_order(*args, **kwargs):
        raise Exception("Test error")

    monkeypatch.setattr(OrderService, "create_order", mock_create_order)

    response = api_client.post(
        "/api/orders/", {"user_id": user.id, "amount": "100.00"}, format="json"
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.data["success"] is False
    assert response.data["error"] == "INTERNAL_ERROR"

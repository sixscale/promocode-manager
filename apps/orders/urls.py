from django.urls import path

from apps.orders.views import OrderViewSet

urlpatterns = [
    path(
        "orders/",
        OrderViewSet.as_view({"post": "create"}),
        name="create-order",
    ),
]

import logging
from typing import Any, Type

from drf_yasg.utils import swagger_auto_schema
from injector import inject
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.orders.exceptions import PromoCodeError
from apps.orders.models import Order
from apps.orders.schemas import ORDER_CREATE_SWAGGER_SCHEMA
from apps.orders.serializers import OrderCreateSerializer, OrderResponseSerializer
from apps.orders.services import OrderService
from apps.users.exceptions import UserNotFoundError

logger: logging.Logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    @inject
    def __init__(self, order_service: OrderService, *args: Any, **kwargs: Any) -> None:
        self.order_service: OrderService = order_service
        super().__init__(*args, **kwargs)

    serializer_class = OrderResponseSerializer

    def get_queryset(self) -> Any:
        return Order.objects.all()

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == "create":
            return OrderCreateSerializer
        return self.serializer_class

    @swagger_auto_schema(**ORDER_CREATE_SWAGGER_SCHEMA)
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: BaseSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data: dict[str, Any] = serializer.validated_data

        try:
            order: Order = self._create_order(validated_data)
            return self._success_response(order)

        except (PromoCodeError, UserNotFoundError, Exception) as e:
            return self._error_response(e)

    def _create_order(self, validated_data: dict[str, Any]) -> Order:
        user_id: int = validated_data["user_id"]
        amount: float = validated_data["amount"]
        promo_code: str | None = validated_data.get("promo_code")
        return self.order_service.create_order(
            user_id=user_id, amount=amount, promo_code=promo_code
        )

    def _success_response(self, order: Order) -> Response:
        response_serializer: OrderResponseSerializer = OrderResponseSerializer(order)
        return Response(
            {"success": True, "data": response_serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def _error_response(self, exception: Exception) -> Response:
        if isinstance(exception, PromoCodeError):
            return Response(
                {
                    "success": False,
                    "error": "PROMO_CODE_ERROR",
                    "message": str(exception),
                },
                status=400,
            )

        if isinstance(exception, UserNotFoundError):
            return Response(
                {
                    "success": False,
                    "error": "USER_NOT_FOUND",
                    "message": str(exception),
                },
                status=404,
            )

        logger.error(f"Internal error: {exception}", exc_info=True)
        return Response(
            {
                "success": False,
                "error": "INTERNAL_ERROR",
                "message": "Внутренняя ошибка сервера",
            },
            status=500,
        )

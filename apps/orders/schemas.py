from drf_yasg import openapi
from rest_framework import status

ORDER_CREATE_REQUEST = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["user_id", "amount"],
    properties={
        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=123),
        "amount": openapi.Schema(
            type=openapi.TYPE_STRING, format="string", example="1500.50"
        ),
        "promo_code": openapi.Schema(
            type=openapi.TYPE_STRING, example="WELCOME2024", nullable=True
        ),
    },
)

ORDER_DATA_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=456),
        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=123),
        "amount": openapi.Schema(type=openapi.TYPE_STRING, example="1500.50"),
        "promo_code": openapi.Schema(
            type=openapi.TYPE_STRING, example="WELCOME2024", nullable=True
        ),
        "final_amount": openapi.Schema(type=openapi.TYPE_STRING, example="1350.50"),
        "created_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="datetime", example="2024-03-15T14:30:00Z"
        ),
    },
)

SUCCESS_RESPONSE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "data": ORDER_DATA_SCHEMA,
    },
)

ERROR_RESPONSE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        "error": openapi.Schema(type=openapi.TYPE_STRING, example="ERROR_CODE"),
        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Описание ошибки"),
    },
)

ORDER_CREATE_SWAGGER_SCHEMA = {
    "operation_summary": "Создание заказа",
    "operation_description": """
    Создает новый заказ для пользователя с возможным применением промокода.
    
    **Логика работы:**
    - Валидация входных данных
    - Применение промокода (если указан)
    - Создание заказа через сервисный слой
    
    **Возможные ошибки:**
    - `PROMO_CODE_ERROR` — невалидный/истекший промокод (400)
    
    - `USER_NOT_FOUND` — пользователь не найден (404)
    
    - `INTERNAL_ERROR` — внутренняя ошибка сервера (500)
    """,
    "request_body": ORDER_CREATE_REQUEST,
    "responses": {
        status.HTTP_201_CREATED: SUCCESS_RESPONSE,
        status.HTTP_400_BAD_REQUEST: ERROR_RESPONSE_SCHEMA,
        status.HTTP_404_NOT_FOUND: ERROR_RESPONSE_SCHEMA,
        status.HTTP_500_INTERNAL_SERVER_ERROR: ERROR_RESPONSE_SCHEMA,
    },
    "tags": ["Orders"],
    "security": [{"Bearer": []}],
}

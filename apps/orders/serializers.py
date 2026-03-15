from decimal import Decimal, InvalidOperation

from rest_framework import serializers

from apps.orders.models import Order


class OrderCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    amount = serializers.CharField(max_length=20)
    promo_code = serializers.CharField(
        max_length=50, required=False, allow_blank=True, allow_null=True
    )

    def validate_amount(self, value: str) -> Decimal:
        try:
            amount = Decimal(value)
        except InvalidOperation:
            raise serializers.ValidationError("Сумма должна быть валидным числом")

        if amount <= 0:
            raise serializers.ValidationError("Сумма заказа должна быть положительной")

        if amount != amount.quantize(Decimal("0.01")):
            raise serializers.ValidationError(
                "Сумма должна иметь не более 2 знаков после запятой"
            )

        return amount


class OrderResponseSerializer(serializers.ModelSerializer):
    promo_code_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user_id",
            "final_amount",
            "promo_code_details",
            "created_at",
        ]

    def get_promo_code_details(self, obj: Order) -> dict | None:
        if obj.promo_code:
            return {
                "code": obj.promo_code.code,
                "discount_percent": str(obj.promo_code.discount_percent),
            }
        return None

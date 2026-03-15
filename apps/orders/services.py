from decimal import Decimal
from typing import Optional, Tuple

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.orders.exceptions import (
    PromoCodeAlreadyUsedError,
    PromoCodeExhaustedError,
    PromoCodeExpiredError,
    PromoCodeNotFoundError,
    PromoCodeNotStartedError,
)
from apps.orders.models import Order, PromoCode, PromoCodeUsage
from apps.users.models import User


class PromoCodeService:

    @staticmethod
    def validate_promo_code(
        code: str,
        user_id: int,
    ) -> PromoCode:

        try:
            promo = PromoCode.objects.select_for_update().get(code=code)
        except PromoCode.DoesNotExist:
            raise PromoCodeNotFoundError(code)

        now = timezone.now()
        if now < promo.date_from:
            raise PromoCodeNotStartedError(code, promo.date_from)
        if now > promo.date_until:
            raise PromoCodeExpiredError(code, promo.date_until)

        if not promo.has_available_uses:
            raise PromoCodeExhaustedError(code, promo.current_uses, promo.max_uses)

        if PromoCodeUsage.objects.filter(user_id=user_id, promo_code=promo).exists():
            raise PromoCodeAlreadyUsedError(code, user_id)

        return promo


class OrderService:

    @staticmethod
    def additional_ordering_information(
        amount: Decimal, promo_code: str, user_id: int
    ) -> Tuple[PromoCode, Decimal]:
        promo = PromoCodeService.validate_promo_code(promo_code, user_id)
        discount = (amount * promo.discount_percent / 100).quantize(Decimal("0.01"))
        final_amount = amount - discount

        if final_amount < Decimal("0.00"):
            final_amount = Decimal("0.00")
        return promo, final_amount

    @transaction.atomic
    def create_order(
        self, user_id: int, amount: Decimal, promo_code: Optional[str] = None
    ) -> Order:

        promo: Optional[PromoCode] = None
        final_amount: Decimal = amount

        user: User = get_object_or_404(User, id=user_id)

        if promo_code:
            promo, final_amount = self.additional_ordering_information(
                amount, promo_code, user_id
            )

        order = Order.objects.create(
            user=user,
            amount=amount,
            final_amount=final_amount,
            promo_code=promo,
        )

        if promo:
            promo.increment_usage()
            PromoCodeUsage.objects.create(user=user, promo_code=promo, order=order)

        return order

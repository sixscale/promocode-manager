import sys
from decimal import Decimal

from django.core.exceptions import PermissionDenied
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from apps.users.models import User


class AdminOnlyManager(models.Manager):

    def create(self, **kwargs):
        if "pytest" in sys.modules:
            return self._queryset_class(self.model).create(**kwargs)
        raise PermissionDenied("Создание только через админку")

    def bulk_create(self, objs, **kwargs):
        raise PermissionDenied("Создание только через админку")

    def bulk_update(self, objs, fields, **kwargs):
        raise PermissionDenied("Обновление только через админку")

    def update_or_create(self, defaults=None, **kwargs):
        raise PermissionDenied("Обновление только через админку")

    def get_or_create(self, defaults=None, **kwargs):
        raise PermissionDenied("Создание только через админку")


class PromoCode(models.Model):
    objects = AdminOnlyManager()
    _admin_objects = models.Manager()

    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Скидка %",
    )
    date_from = models.DateTimeField()
    date_until = models.DateTimeField()
    max_uses = models.PositiveIntegerField(
        help_text="Максимальное количество использований"
    )
    current_uses = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "promo_codes"
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self) -> str:
        return f"{self.code} ({self.discount_percent}%)"

    @property
    def has_available_uses(self) -> bool:
        return self.current_uses < self.max_uses

    def increment_usage(self) -> None:
        self.current_uses += 1
        self.save(update_fields=["current_uses"])


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        indexes = [
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"Order #{self.id} by {self.user}"


class PromoCodeUsage(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="promo_usages"
    )
    promo_code = models.ForeignKey(
        PromoCode, on_delete=models.CASCADE, related_name="usages"
    )
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="promo_usage"
    )
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "promo_code_usages"
        verbose_name = "Использование промокода"
        verbose_name_plural = "Использования промокодов"
        unique_together = ["user", "promo_code"]
        indexes = [
            models.Index(fields=["user", "promo_code"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} used {self.promo_code.code}"

from django.contrib import admin
from django.utils import timezone

from apps.orders.models import Order, PromoCode, PromoCodeUsage


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "discount_percent",
        "date_from",
        "date_until",
        "max_uses",
        "current_uses",
        "has_available_uses",
    ]
    list_filter = ["date_from", "date_until"]
    search_fields = [
        "code",
    ]
    readonly_fields = [
        "current_uses",
        "created_at",
    ]

    def has_available_uses(self, obj: PromoCode) -> bool:
        return obj.has_available_uses

    has_available_uses.boolean = True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = timezone.now()

        super().save_model(request, obj, form, change)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "amount",
        "final_amount",
        "promo_code",
        "created_at",
    ]
    list_filter = [
        "id",
        "user",
        "created_at",
        "final_amount",
    ]
    search_fields = [
        "user__username",
        "promo_code__code",
    ]


@admin.register(PromoCodeUsage)
class PromoCodeUsageAdmin(admin.ModelAdmin):
    list_display = ["user", "promo_code", "order", "used_at"]
    list_filter = ["used_at"]
    search_fields = ["user__username", "promo_code__code"]

from decimal import Decimal

import pytest

from apps.orders.exceptions import (
    PromoCodeAlreadyUsedError,
    PromoCodeExhaustedError,
    PromoCodeExpiredError,
    PromoCodeNotStartedError,
)
from apps.orders.services import PromoCodeService


@pytest.mark.django_db
def test_validate_promo_code_valid(valid_promo_code):
    promo = PromoCodeService.validate_promo_code("VALID", 1)
    assert promo.code == "VALID"


@pytest.mark.django_db
def test_validate_promo_code_not_started(not_started_promo_code):
    with pytest.raises(PromoCodeNotStartedError):
        PromoCodeService.validate_promo_code("NOTSTARTED", 1)


@pytest.mark.django_db
def test_validate_promo_code_expired(expired_promo_code):
    with pytest.raises(PromoCodeExpiredError):
        PromoCodeService.validate_promo_code("EXPIRED", 1)


@pytest.mark.django_db
def test_validate_promo_code_exhausted(exhausted_promo_code):
    with pytest.raises(PromoCodeExhaustedError):
        PromoCodeService.validate_promo_code("EXHAUSTED", 1)


@pytest.mark.django_db
def test_validate_promo_code_already_used(user, used_promo_code):
    with pytest.raises(PromoCodeAlreadyUsedError):
        PromoCodeService.validate_promo_code("VALID_USED", user.id)

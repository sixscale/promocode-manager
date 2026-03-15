from dataclasses import dataclass


@dataclass
class PromoCodeError(Exception):
    code: str

    def __str__(self) -> str:
        return f"Ошибка промокода '{self.code}'"


@dataclass
class PromoCodeNotFoundError(PromoCodeError):
    def __str__(self) -> str:
        return f"Промокод '{self.code}' не найден"


@dataclass
class PromoCodeNotStartedError(PromoCodeError):
    date_from: str

    def __str__(self) -> str:
        return (
            f"Промокод '{self.code}' ещё не активен (будет доступен с {self.date_from})"
        )


@dataclass
class PromoCodeExpiredError(PromoCodeError):
    date_until: str

    def __str__(self) -> str:
        return f"Промокод '{self.code}' истёк (действовал до {self.date_until})"


@dataclass
class PromoCodeExhaustedError(PromoCodeError):
    current_uses: int
    max_uses: int

    def __str__(self) -> str:
        return f"Промокод '{self.code}' исчерпан (использован {self.current_uses} из {self.max_uses})"


@dataclass
class PromoCodeAlreadyUsedError(PromoCodeError):
    user_id: int

    def __str__(self) -> str:
        return f"Пользователь id={self.user_id}, уже использовал промокод '{self.code}'"

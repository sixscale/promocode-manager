from dataclasses import dataclass


@dataclass
class UserError(Exception):
    pass


@dataclass
class UserNotFoundError(UserError):
    def __str__(self) -> str:
        return f"Пользователь не найден!"

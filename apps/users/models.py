from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"{self.username} (id={self.id})"

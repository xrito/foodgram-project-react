from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]
    USERNAME_FIELD = 'username'
    email = models.EmailField(max_length=255, unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    subscribing = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscribing'],
                name='unique_user_subscribing'
            )
        ]

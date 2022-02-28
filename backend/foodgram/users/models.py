from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]
    USERNAME_FIELD = 'username'
    email = models.EmailField(max_length=255, unique=True)


    class Meta:
        ordering = ('id',)

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
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscribing'],
                name='unique_user_subscribing'
            )
        ]

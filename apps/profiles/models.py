from django.db import models
from account.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_sync_date = models.DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Профили"
        verbose_name_plural = "Профиль"

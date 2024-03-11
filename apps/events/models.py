from django.db import models
from django.contrib.auth import get_user_model

from apps.events_category.models import EventsCategory

User = get_user_model()


class Events(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название мероприятия")
    image = models.ImageField(upload_to="events_photo/", verbose_name="Фото")
    video = models.FileField(upload_to="events_videos/", verbose_name="Видео")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    paid = models.BooleanField(default=False, verbose_name="Платное")
    paid_reservation = models.BooleanField(
        default=False, verbose_name="Платное бронирование"
    )
    reservation_payment_percentage = models.IntegerField(
        verbose_name="Процент оплаты бронирования"
    )
    address = models.CharField(max_length=200, verbose_name="Адрес")
    online_screening = models.BooleanField(default=False, verbose_name="Онлайн-показ")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="events", verbose_name="Автор"
    )
    category = models.ForeignKey(
        EventsCategory,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name="Категория",
    )
    auto_publication = models.BooleanField(
        default=False, verbose_name="Авто публикация"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создание")
    qr_code = models.TextField(verbose_name="QR-code")
    
    
    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = "Мероприятия"
        verbose_name_plural = "Мероприятия"
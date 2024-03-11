from django.db import models
from autoslug import AutoSlugField


class EventsCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", unique=True)
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    def __str__(self):
        return self.title

    def get_all_subcategories(self):
        return EventsCategory.objects.filter(parent_category=self)

    class Meta:
        verbose_name = " Категория мероприятий"
        verbose_name_plural = "Категория мероприятий"

from rest_framework import serializers

from .models import Events
from apps.events_category.models import EventsCategory


class EventSerializers(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=EventsCategory.objects.all())

    class Meta:
        model = Events
        fields = "__all__"

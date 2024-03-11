from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Events
from .serializers import EventSerializers

class EventsModelViewset(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]
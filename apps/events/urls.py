from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import EventsModelViewset

router = DefaultRouter()
router.register("", EventsModelViewset)


urlpatterns = [
    path("", include(router.urls))
]
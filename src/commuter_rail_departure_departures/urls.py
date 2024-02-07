from django.urls import path
from commuter_rail_departure_departures.views import *

from rest_framework import routers
router = routers.SimpleRouter()

router.register(r"stop", StopReadOnlyViewSet)

urlpatterns = []

urlpatterns += router.urls
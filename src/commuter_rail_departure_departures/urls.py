from django.urls import path
from commuter_rail_departure_departures.views import *

from rest_framework import routers
router = routers.SimpleRouter()

router.register(r"stop-names", StopReadOnlyViewSet)

urlpatterns = [
    path("api/<str:mbta_id>/", DeparturesApiView.as_view()),
    path("api/", DeparturesApiView.as_view())
]

urlpatterns += router.urls
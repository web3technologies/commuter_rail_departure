from rest_framework.viewsets import ReadOnlyModelViewSet

from commuter_rail_departure_departures.models import Stop
from commuter_rail_departure_departures.serializer import StopSerializer


class StopReadOnlyViewSet(ReadOnlyModelViewSet):

    queryset = Stop.stops.with_child_count().order_by("name")
    serializer_class = StopSerializer
    lookup_field = "mbta_id"


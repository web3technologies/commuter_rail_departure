from datetime import datetime
import pytz
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from commuter_rail_departure_departures.processor.departure_processor import DepartureProcessor
from commuter_rail_departure_departures.models import Stop
from commuter_rail_departure_departures.serializer import StopSerializer


class StopReadOnlyViewSet(ReadOnlyModelViewSet):

    queryset = Stop.stops.with_child_count().order_by("name")
    serializer_class = StopSerializer
    lookup_field = "mbta_id"
    eastern = pytz.timezone('US/Eastern')
    
    def retrieve(self, request, *args, **kwargs):
        stop = get_object_or_404(Stop, mbta_id=kwargs.get("mbta_id"))
        eastern_time = datetime.now(self.eastern)
        data = DepartureProcessor.process_data(stop.mbta_id, eastern_time)
        return_data = {
            "departures": data,
            "eastern_time": eastern_time.strftime("%I:%M:%S %p"),
            "eastern_date": eastern_time.strftime("%Y-%m-%d")
        }
        
        return Response(return_data, HTTP_200_OK)


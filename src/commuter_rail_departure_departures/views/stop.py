from datetime import timedelta, datetime
import pytz

from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from commuter_rail_departure_core.client import mbta_client
from commuter_rail_departure_departures.models import Route, Stop
from commuter_rail_departure_departures.serializer import StopSerializer


class StopReadOnlyViewSet(ReadOnlyModelViewSet):

    queryset = Stop.stops.with_child_count().order_by("name")
    serializer_class = StopSerializer
    lookup_field = "mbta_id"
    
    def retrieve(self, request, *args, **kwargs):
        
        stop = self.get_object()
        eastern = pytz.timezone('US/Eastern')
        eastern_time = datetime.now(eastern)
        eastern_date = eastern_time.strftime("%Y-%m-%d")
        current_eastern_time = eastern_time.strftime("%I:%M:%S %p")
    
        data = []
        routes = Route.objects.filter(type="2")
        
        route_set = set(routes.values_list("mbta_id", flat=True))
        
        predictions = mbta_client.get_predictions(stop_id=stop.mbta_id)
        trip_id_to_prediction_mapping = {(prediction.trip_id, prediction.stop_id): prediction for prediction in predictions if prediction.route_id in route_set}
        
        schedules = mbta_client.get_schedules(stop_id=stop.mbta_id) 
        trip_id_to_schedule_mapping = {(schedule.trip_id, schedule.stop_id): schedule for schedule in schedules if schedule.route_id in route_set} 
        trip_cache = {}
        for _, schedule in trip_id_to_schedule_mapping.items():
            if not schedule.departure_time or eastern_time > schedule.departure_time:
                continue
            if (schedule.trip_id, schedule.stop_id) in trip_id_to_prediction_mapping:
                prediction = trip_id_to_prediction_mapping[(schedule.trip_id, schedule.stop_id)]
                if prediction.departure_time:
                    time_diff = prediction.departure_time - schedule.departure_time
                    if time_diff < timedelta(minutes=0):
                        status = "EARLY"
                    elif time_diff >= timedelta(minutes=0) and time_diff < timedelta(minutes=3):
                        status = "ON-TIME"
                    else:
                        status = "LATE"
                else:
                    status = "unkown"
                if prediction.trip_id not in trip_cache:
                    trip_cache[prediction.trip_id] = mbta_client.get_trip(prediction.trip_id)
                append_data = \
                    {
                        "carrier": "MBTA",
                        "departure_time": prediction.departure_time if prediction.departure_time else "---",
                        "arrival_time": prediction.arrival_time if prediction.arrival_time else "---",
                        "destination": trip_cache[prediction.trip_id].headsign, 
                        "vehicle_id": prediction.vehicle_id, 
                        "status": prediction.schedule_relationship if prediction.schedule_relationship == "ADDED" else status,
                        "has_prediction": True
                    }
            elif not schedule.departure_time:
                status = "FINAL-STOP"
            else:
                status = "ON-TIME"
                append_data = \
                {
                        "carrier": "MBTA",
                        "departure_time": schedule.departure_time if schedule.departure_time else "---",
                        "arrival_time": schedule.arrival_time if schedule.arrival_time else "---",
                        "destination": schedule.stop_headsign, 
                        "vehicle_id": "Not yet available", 
                        "status": status,
                        "has_prediction": False
                    }
            data.append(append_data)
        data.sort(key=lambda predictionData: (predictionData["departure_time"]))

    
        return_data = {
            "departures": data,
            "eastern_time": current_eastern_time,
            "eastern_date": eastern_date
        }
        
        return Response(return_data, HTTP_200_OK)


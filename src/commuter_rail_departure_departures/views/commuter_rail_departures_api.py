from datetime import datetime, timedelta
import pytz

from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import APIView


from commuter_rail_departure_departures.models import Route, Stop
from commuter_rail_departure_core.client import mbta_client


class DeparturesApiView(APIView):
    
    def get_data(self, current_eastern_time, stop_mbta_id):
        data = []
        routes = Route.objects.filter(type="2")
        trip_cache = {}
        stop_cache = {}
        for route in routes:
            predictions = mbta_client.get_predictions(route.mbta_id, stop_id=stop_mbta_id)
            if not predictions:
                continue
            schedules = mbta_client.get_schedules(route.mbta_id, stop_id=stop_mbta_id)
            trip_id_to_schedule_mapping = {(schedule.trip_id, schedule.stop_id): schedule for schedule in schedules}        
            for prediction in predictions:
                print(prediction)
                
                if not prediction.departure_time:
                    continue
                    
                if current_eastern_time > prediction.departure_time:
                    continue

                scheduled_departure = None
                if (prediction.trip_id, prediction.stop_id) in trip_id_to_schedule_mapping and prediction.departure_time:
                    scheduled_departure = trip_id_to_schedule_mapping[(prediction.trip_id, prediction.stop_id)]
                    time_diff = prediction.departure_time - scheduled_departure.departure_time
                    if time_diff < timedelta(minutes=0):
                        status = "EARLY"
                    elif time_diff >= timedelta(minutes=0) and time_diff < timedelta(minutes=3):
                        status = "ON-TIME"
                    else:
                        status = "LATE"
                else:
                    status = "Final Stop"
                        
                if prediction.trip_id not in trip_cache:
                    trip_cache[prediction.trip_id] = mbta_client.get_trip(prediction.trip_id)
                if prediction.stop_id not in stop_cache:
                    stop_cache[prediction.stop_id] = Stop.objects.get(mbta_id=prediction.stop_id)
                
                data.append(
                    [
                        "MBTA",
                        stop_cache[prediction.stop_id].name,
                        prediction.arrival_time_str if prediction.arrival_time_str else "---", 
                        prediction.departure_time_str if prediction.departure_time_str else "---",
                        scheduled_departure.departure_time_str if scheduled_departure else "---",
                        trip_cache[prediction.trip_id].headsign, 
                        prediction.vehicle_id, 
                        prediction.schedule_relationship if prediction.schedule_relationship == "ADDED" else status,
                    ] 
                )
        data.sort(key=lambda predictionData: (predictionData[3]))
        return data
    
    def get(self, *args, **kwargs):
        return_data = {}
        eastern = pytz.timezone('US/Eastern')
        eastern_time = datetime.now(eastern)
        return_data['departures'] = self.get_data(eastern_time, kwargs.get("mbta_id"))
        return_data["eastern_date"] = eastern_time.strftime("%Y-%m-%d ")
        return_data["eastern_time"] = eastern_time.strftime("%I:%M:%S %p")
        return Response(return_data, HTTP_200_OK)
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
        for route in routes:
            predictions = mbta_client.get_predictions(route.mbta_id, stop_id=stop_mbta_id)
            trip_id_to_prediction_mapping = {(prediction.trip_id, prediction.stop_id): prediction for prediction in predictions}        
            if not predictions:
                continue
            schedules = mbta_client.get_schedules(route.mbta_id, stop_id=stop_mbta_id)
            for schedule in schedules:
                
                if not schedule.departure_time or current_eastern_time > schedule.departure_time:
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
                            "destination": schedule.stop_headsign, 
                            "vehicle_id": "Not yet available", 
                            "status": status,
                            "has_prediction": False
                        }
                data.append(append_data)
        data.sort(key=lambda predictionData: (predictionData["departure_time"]))
        return data
    
    def get(self, *args, **kwargs):
        return_data = {}
        eastern = pytz.timezone('US/Eastern')
        eastern_time = datetime.now(eastern)
        return_data['departures'] = self.get_data(eastern_time, kwargs.get("mbta_id"))
        return_data["eastern_date"] = eastern_time.strftime("%Y-%m-%d")
        return_data["eastern_time"] = eastern_time.strftime("%I:%M:%S %p")
        return Response(return_data, HTTP_200_OK)

from datetime import datetime, timedelta
import pytz

from django.views.generic import TemplateView

from commuter_rail_departure_departures.models import Stop
from commuter_rail_departure_core.client import mbta_client


class DeparturesView(TemplateView):
    template_name = 'commuter_rail_departure_departures/departures.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eastern = pytz.timezone('US/Eastern')
        eastern_time = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S")
        context['departures'] = self.get_data()
        context["eastern_time"] = eastern_time
        return context
    
    def get_data(self):
        data = []
        stop = Stop.objects.get(mbta_id="place-north")
        routes = mbta_client.get_routes(types=["2"])
        for route in routes:
            predictions = mbta_client.get_predictions(stop.mbta_id, route.id)
            if not predictions:
                continue
            schedules = mbta_client.get_schedules(stop.mbta_id, route.id)
            trip_id_to_schedule_mapping = {schedule.trip_id: schedule for schedule in schedules}        
            for prediction in predictions:
                print(prediction.departure_time)
                if prediction.departure_time is None:
                    continue
                print(prediction)
                vehicle = mbta_client.get_vehicle(prediction.vehicle_id)
                trip = mbta_client.get_trip(prediction.trip_id)
                if prediction.trip_id in trip_id_to_schedule_mapping:
                    scheduled_departure = trip_id_to_schedule_mapping[prediction.trip_id].departure_time
                    time_diff = prediction.departure_time - scheduled_departure
                    if time_diff < timedelta(minutes=0):
                        status = "EARLY"
                    elif time_diff >= timedelta(minutes=0) and time_diff < timedelta(minutes=3):
                        status = "ON-TIME"
                    else:
                        status = "LATE"
                data.append(
                ["MBTA", 
                    prediction.departure_time,
                    trip.headsign, 
                    vehicle.id, 
                    prediction.schedule_relationship if prediction.schedule_relationship == "ADDED" else status
                    ] 
                )
        data.sort(key=lambda predictionData: predictionData[1])
        return data

from datetime import timedelta
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'commuter_rail_departure.settings.settings')
django.setup()
from django.conf import settings

from commuter_rail_departure_core.client import MBTAClient


client = MBTAClient(settings.MBTA_KEY)

def get_data():
    data = []

    stop = client.get_stop("place-north")
    routes = client.get_routes(types=["0","1","2"])
    for route in routes:
        predictions = client.get_predictions(stop.id, route.id)
        schedules = client.get_schedules(stop.id, route.id)
        trip_id_to_schedule_mapping = {schedule.trip_id: schedule for schedule in schedules}        
        for prediction in predictions:
            print(prediction.departure_time)
            if prediction.departure_time is None:
                continue
            vehicle = client.get_vehicle(prediction.vehicle_id)
            trip = client.get_trip(prediction.trip_id)
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

if __name__ == "__main__":
    get_data()
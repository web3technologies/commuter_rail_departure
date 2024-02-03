import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'commuter_rail_departure.settings.settings')
django.setup()
from django.conf import settings

from datetime import datetime
import pytz

from commuter_rail_departure_core.client import MBTAClient


client = MBTAClient(settings.MBTA_KEY)

def get_data():

    routes = client.get_routes(types=["0","1","2"])
    eastern = pytz.timezone('US/Eastern')
    eastern_time = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S")
    
    for route in routes:
        schedule_mapping = {}
        schedule_data = client.get_schedules(route.id)
        for schedule in schedule_data:
            schedule_mapping[schedule.trip_id] = schedule
    
        prediction_data = client.get_predictions(route.id)
        for vehicle, predictions in prediction_data.items():
            print(route, vehicle, eastern_time)
            print("arrival time", "departure time", "trip id")
            for prediction in predictions:
                print(prediction.arrival_time_str, prediction.departure_time_str, prediction.trip_id)
                if prediction.trip_id in schedule_mapping:
                    schedule = schedule_mapping[prediction.trip_id]
                    if (
                        schedule.route_id == prediction.route_id and
                        schedule.stop_id == prediction.stop_id  
                    ):
                        print(f"schedule: {schedule.arrival_time_str}, {schedule.departure_time_str}")
                        print(f"prediction: {prediction.arrival_time_str}, {prediction.departure_time_str}")
                        pass
            print()
        


if __name__ == "__main__":
    get_data()
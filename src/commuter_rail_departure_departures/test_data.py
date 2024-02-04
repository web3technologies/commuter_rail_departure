from datetime import timedelta
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
    eastern = pytz.timezone('US/Eastern')
    eastern_time = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S")
    stop = client.get_stop("place-north")
    routes = client.get_routes(types=["0","1","2"])
    for route in routes:
        predictions = client.get_predictions(stop.id, route.id)
        for pred in predictions:
            if pred.departure_time is None:
                continue
            vehicle = client.get_vehicle(pred.vehicle_id)
            trip = client.get_trip(pred.trip_id)
            print("MBTA", pred.departure_time_str, trip.headsign, vehicle.id, "TBD", vehicle.current_status)
    
        
        


if __name__ == "__main__":
    get_data()
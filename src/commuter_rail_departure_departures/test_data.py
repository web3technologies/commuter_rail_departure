import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'commuter_rail_departure.settings.settings')
django.setup()

import requests
import pprint
from datetime import datetime
import pytz
from django.conf import settings

from commuter_rail_departure_core.client import MBTAClient


client = MBTAClient(settings.MBTA_KEY)

def get_data():

    routes = client.get_routes(types=["0","1","2"])

    for route in routes:
        predictions = client.get_predictions(route.id)
        for prediction in predictions:
            print(prediction)


if __name__ == "__main__":
    get_data()
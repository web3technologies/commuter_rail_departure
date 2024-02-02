import requests
import pprint
from datetime import datetime
import pytz


def get_routes():

    BASE_URL = "https://api-v3.mbta.com/routes?filter[type]=0,1,2`"
    res = requests.get(BASE_URL)
    data = res.json().get("data")
    desc_mapping = {}
    type_set = set()
    ids = []

    for route in data:
        desc = route.get("attributes").get("description")
        type_set.add(route.get("attributes").get("type"))
        desc_mapping[desc] = desc_mapping.get(desc, 0) + 1
        pprint.pprint(route)
        ids.append(route.get("id"))
    print(ids)

def get_predictions():
    # base_url = "https://api-v3.mbta.com/predictions/?filter[route]=CR-Kingston"
    base_url = "https://api-v3.mbta.com/schedules/?filter[route]=CR-Kingston"
    res = requests.get(base_url)
    data = res.json()
    print("Departure Time", "Arrival Time")
    for prediction in data.get("data"):
        attrs = prediction.get("attributes")
        rels = prediction.get("relationships").get("trip").get("data").get("id")
        print(rels)
        print(format_date(attrs.get("departure_time")), format_date(attrs.get("arrival_time")))


        
def format_date(date_str:str):
    if not date_str:
        return date_str
    date_obj = datetime.fromisoformat(date_str)
    eastern = pytz.timezone('US/Eastern')
    eastern_time = date_obj.astimezone(eastern)
    formatted_time = eastern_time.strftime("%I:%M:%S %p")
    return formatted_time

if __name__ == "__main__":
    get_predictions()
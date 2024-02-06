import pytest
from django.conf import settings
import json


from commuter_rail_departure_core.client.mbta import MBTAClient


@pytest.fixture(scope="function")
def mock_mbta_client(monkeypatch):
     
    def __return_dict(filename):
        with open(f"{settings.MOCK_DATA}{filename}", "r") as file:
            data = json.load(file)
            return data 
        
    def _request(self, endpoint: str, params:dict = None) -> dict:
        if endpoint == "predictions":
            return __return_dict("predictions.json")
        elif endpoint == "routes":
            return __return_dict("routes.json")
        elif endpoint == "schedules":
            return __return_dict('schedules.json')
        elif endpoint == "stops":
            return __return_dict("stops.json")
        elif "trip" in endpoint:
            return __return_dict("trip.json")
        else:
            raise Exception("Invalid mock endpoint")
            

    monkeypatch.setattr(MBTAClient, "_request", _request)

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
        
    def __default_dict():
        return {"data": [], "jsonapi": []}
        
    def _request(self, endpoint: str, params:dict = None) -> dict:
        if endpoint == "predictions":
            if params["filter[stop]"] == "place-north":
                file = "predictions-place-north.json"
            elif params["filter[stop]"] == "place-sstat":
                file = "predictions-place-sstat.json"
            else:
                return __default_dict()
            return __return_dict(file)
        elif endpoint == "routes":
            return __return_dict("routes.json")
        elif endpoint == "schedules":
            if params["filter[stop]"] == "place-north":
                file = "schedules-place-north.json"
            elif params["filter[stop]"] == "place-sstat":
                file = "schedules-place-sstat.json"
            else:
                return __default_dict()
            return __return_dict(file)
        elif endpoint == "stops":
            return __return_dict("stops.json")
        elif endpoint == "trips":
            return __return_dict("trips.json")
        elif endpoint == "vehicles":
            return __return_dict("vehicles.json")
        else:
            raise Exception("Invalid mock endpoint")
            

    monkeypatch.setattr(MBTAClient, "_request", _request)

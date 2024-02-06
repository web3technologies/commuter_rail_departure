import pytest
from datetime import datetime, timezone
from typing import List, Optional
from django.conf import settings
from collections import defaultdict
import json


from commuter_rail_departure_core.client import mbta

from commuter_rail_departure_core.types import (
    PredictionData, 
    RouteData, 
    ScheduleData, 
    StopData,
    TripData,
    VehicleData
) 

@pytest.fixture(scope="function")
def mock_mbta_client(monkeypatch):
    
    class MockMBTAClient:
        def __init__(self, mbta_access_key: str) -> None:
            self.mbta_access_key = mbta_access_key
            self.headers = {"x-api-key": self.mbta_access_key}
            
        def __return_dict(self, filename):
            with open(f"{settings.MOCK_DATA}{filename}", "r") as file:
                data = json.load(file)
                return data 
            
        def get_predictions(self, route_id:str, stop_id:Optional[str]="") -> defaultdict[List[PredictionData]]:
            data = self.__return_dict("predictions.json")
            predictions = [PredictionData.from_dict(item) for item in data.get("data", [])]
            predictions.sort(key=lambda prediction: prediction.departure_time or datetime.max.replace(tzinfo=timezone.utc))
            return predictions

        def get_routes(self, types: Optional[List[int]] = None) -> List[RouteData]:
            """Gets a list of possible routes."""
            data = self.__return_dict("routes.json")
            routes = [RouteData.from_dict(item) for item in data.get("data", [])]
            return routes
        
        def get_schedules(self, route_id:str, stop_id:Optional[str]="") -> defaultdict[List[ScheduleData]]:
            """Gets a list of schedules for a route id"""
            data = self.__return_dict('schedules')
            schedules = [ScheduleData.from_dict(item) for item in data.get("data", [])]
            return schedules

        def get_stop(self, stop_id:str) -> StopData:
            stop = ...
            return stop
        
        def get_stops(self) -> List[StopData]:
            data = self.__return_dict("stops.json")
            return [StopData.from_dict(obj) for obj in data.get("data")]
        
        def get_trip(self, trip_id:str) -> TripData:
            data = self.__return_dict("trip.json")
            return TripData.from_dict(data.get("data"))
        
        def get_vehicle(self, vehicle_id:str) -> VehicleData:
            data = []
            return VehicleData.from_dict(data.get("data"))
            

    monkeypatch.setattr(mbta, "MBTAClient", MockMBTAClient)

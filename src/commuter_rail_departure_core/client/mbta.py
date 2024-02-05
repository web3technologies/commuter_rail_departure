from collections import defaultdict
from datetime import datetime, timezone
from typing import List, Optional

import requests

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from commuter_rail_departure_core.types import (
    PredictionData, 
    RouteData, 
    ScheduleData, 
    StopData,
    TripData,
    VehicleData
) 


class MBTAClient:
    base_url = "https://api-v3.mbta.com"
    
    def __init__(self, mbta_access_key: str) -> None:
        self.mbta_access_key = mbta_access_key
        self.headers = {"x-api-key": self.mbta_access_key}
    
    def _request(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Generic method to handle API requests."""
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        return {}

    def get_predictions(self, stop_id:str, route_id:str) -> defaultdict[List[PredictionData]]:
        params = {'filter[stop]': stop_id, 'filter[route]': route_id}
        data = self._request('predictions', params)
        predictions = [PredictionData.from_dict(item) for item in data.get("data", [])]
        predictions.sort(key=lambda prediction: prediction.departure_time or datetime.max.replace(tzinfo=timezone.utc))
        return predictions

    def get_routes(self, types: Optional[List[int]] = None) -> List[RouteData]:
        """Gets a list of possible routes."""
        params = {}
        if types:
            params['filter[type]'] = ','.join(map(str, types))
        data = self._request("routes", params)
        routes = [RouteData.from_dict(item) for item in data.get("data", [])]
        return routes
    
    def get_schedules(self, stop_id:str, route_id:str) -> defaultdict[List[ScheduleData]]:
        """Gets a list of schedules for a route id"""
        params = {'filter[stop]': stop_id, 'filter[route]': route_id}
        data = self._request('predictions', params)
        schedules = [ScheduleData.from_dict(item) for item in data.get("data", [])]
        return schedules

    def get_stop(self, stop_id:str) -> StopData:
        data = self._request(f"stops/{stop_id}")
        return StopData.from_dict(data.get("data"))
    
    def get_stops(self) -> List[StopData]:
        data = self._request(f"stops/")
        return [StopData.from_dict(obj) for obj in data.get("data")]
    
    def get_trip(self, trip_id:str) -> TripData:
        data = self._request(f"trips/{trip_id}")
        return TripData.from_dict(data.get("data"))
    
    def get_vehicle(self, vehicle_id:str) -> VehicleData:
        data = self._request(f"vehicles/{vehicle_id}")
        return VehicleData.from_dict(data.get("data"))


mbta_client = SimpleLazyObject(lambda: MBTAClient(settings.MBTA_KEY))
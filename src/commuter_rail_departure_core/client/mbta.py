from collections import defaultdict
from datetime import datetime, timezone
from typing import List, Optional

import requests

from commuter_rail_departure_core.types import PredictionData, RouteData, ScheduleData 


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
    
    def __get_grouped_data(self, vehicle_data):
        grouped_vehicles = defaultdict(list)
        for prediction in vehicle_data:
            grouped_vehicles[prediction.vehicle_id].append(prediction)
        datetime_max_tz_aware = datetime.max.replace(tzinfo=timezone.utc)
        for vehicle_id in grouped_vehicles:
            grouped_vehicles[vehicle_id].sort(key=lambda prediction: (
                prediction.arrival_time or datetime_max_tz_aware,
                prediction.departure_time or datetime_max_tz_aware
            ))
        return grouped_vehicles
    
    def get_routes(self, types: Optional[List[int]] = None) -> List[RouteData]:
        """Gets a list of possible routes."""
        params = {}
        if types:
            params['filter[type]'] = ','.join(map(str, types))
        data = self._request("routes", params)
        routes = [RouteData.from_dict(item) for item in data.get("data", [])]
        return routes
    
    def get_schedules(self, route_id:str) -> defaultdict[List[ScheduleData]]:
        """Gets a list of schedules for a route id"""
        params = {'filter[route]': route_id}
        data = self._request('predictions', params)
        schedules = [ScheduleData.from_dict(item) for item in data.get("data", [])]
        return schedules

    def get_predictions(self, route_id:str) -> defaultdict[List[PredictionData]]:
        params = {'filter[route]': route_id}
        data = self._request('predictions', params)
        predictions = [PredictionData.from_dict(item) for item in data.get("data", [])]
        grouped_vehicles = self.__get_grouped_data(predictions)
        return grouped_vehicles

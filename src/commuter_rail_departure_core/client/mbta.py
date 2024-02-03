from typing import List, Optional
import requests

from commuter_rail_departure_core.types import Route, Prediction


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
    
    def get_routes(self, types: Optional[List[int]] = None) -> List[Route]:
        """Gets a list of possible routes."""
        params = {}
        if types:
            params['filter[type]'] = ','.join(map(str, types))
        
        data = self._request("routes", params)
        routes = []
        for item in data.get('data', []):
            routes.append(Route.from_dict(item))
        return routes
    
    def get_predictions(self, id:str, sort:bool = False) ->List[Prediction]:
        params = {'filter[route]': id}
        data = self._request('predictions', params)
        predictions = []
        for item in data.get("data", []):
            predictions.append(Prediction.from_dict(item))
            
        return predictions

import pytest
import json

from django.conf import settings

from commuter_rail_departure_departures.models import Stop, Route

from commuter_rail_departure_core.client import mbta_client
from commuter_rail_departure_core.types import (
    PredictionData, 
    RouteData, 
    ScheduleData, 
    StopData,
    TripData,
    VehicleData
) 


@pytest.mark.django_db
class TestMbtaClient:
    
    def test_get_schedule_data(self, mock_mbta_client):
        stop_id="place-north"
        schedules = mbta_client.get_schedules(stop_id)
        with open(f"{settings.MOCK_DATA}schedules-place-north.json", "r") as file:
            data = json.load(file)
                
        assert len(schedules) == len(data.get("data")), "The number of schedules does not match"
        for schedule in schedules:
            assert isinstance(schedule, ScheduleData), "Schedule object is not an instance of ScheduleData"
            
    def test_get_predictions(self, mock_mbta_client):
        stop_id="place-north"
        predictions = mbta_client.get_predictions(stop_id)
        with open(f"{settings.MOCK_DATA}predictions-place-north.json", "r") as file:
            data = json.load(file)
                
        assert len(predictions) == len(data.get("data")), "The number of predictions does not match"
        for prediction in predictions:
            assert isinstance(prediction, PredictionData), "Prediction object is not an instance of PredictionData"
            
            
    def test_get_route_data(self, mock_mbta_client):
        routes = mbta_client.get_routes(types=["2"])
        with open(f"{settings.MOCK_DATA}routes.json", "r") as file:
            data = json.load(file)
                
        assert len(routes) == len(data.get("data")), "The number of routes does not match"
        for route in routes:
            assert isinstance(route, RouteData), "Route object is not an instance of RouteData"
            

    def test_get_stop_data(self, mock_mbta_client):
        stops = mbta_client.get_stops()
        with open(f"{settings.MOCK_DATA}stops.json", "r") as file:
            data = json.load(file)
                
        assert len(stops) == len(data.get("data")), "The number of stops does not match"
        for stop in stops:
            assert isinstance(stop, StopData), "Stop object is not an instance of StopData"
            
    def test_get_trips_data(self, mock_mbta_client):
        Route.routes.create_from_mbta_client()
        routes = Route.objects.filter(type=2)
        route_set = set(routes.values_list("mbta_id", flat=True))
        trips = mbta_client.get_trips(route_set)
        with open(f"{settings.MOCK_DATA}trips.json", "r") as file:
            data = json.load(file)
        
        assert len(trips) == len(data.get("data")), "The number of trips does not match"
        for trip in trips:
            assert isinstance(trip, TripData), "Trip object is not an instance of TripData"
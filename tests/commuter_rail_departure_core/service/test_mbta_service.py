from django.conf import settings
import pytest
import json


from commuter_rail_departure_core.service import mbta_service
from commuter_rail_departure_core.types import (
    RouteData, 
    PredictionData, 
    ScheduleData, 
    TripData, 
    VehicleData 
)
from commuter_rail_departure_departures.models import Route


@pytest.mark.django_db
class TestMbtaService:
    
    def test_service_retrieves_correct_routes(self, mock_mbta_client, create_stop_and_route):
        expected_routes = set(Route.objects.filter(type=2).values_list("mbta_id", flat=True))
        service_routes = mbta_service.get_route_set()
        assert expected_routes == service_routes
        
    def test_service_retrieves_correct_predictions(self, mock_mbta_client, create_stop_and_route):
        service_routes = mbta_service.get_route_set()
        stop_id = "place-sstat"
        with open(f"{settings.MOCK_DATA}predictions-{stop_id}.json", "r") as file:
            data = json.load(file)
        expected_predictions = []
        for prediction in data.get("data"):
            if prediction.get("relationships").get("route").get("data").get("id") in service_routes:
                expected_predictions.append(PredictionData.from_dict(prediction))
        service_predictions = mbta_service.get_predictions(stop_id, service_routes)
        
        expected_predictions.sort(key=lambda pred: pred.id)
        service_predictions.sort(key=lambda pred: pred.id)
        assert len(service_predictions) == len(expected_predictions)
        for expected, service in zip(expected_predictions, service_predictions):
            assert expected.id == service.id
             
    def test_service_retrieves_correct_schedules(self, mock_mbta_client, create_stop_and_route):
        service_routes = mbta_service.get_route_set()
        stop_id = "place-sstat"
        with open(f"{settings.MOCK_DATA}schedules-{stop_id}.json", "r") as file:
            data = json.load(file)
        expected_schedules = []
        for schedule in data.get("data"):
            if schedule.get("relationships").get("route").get("data").get("id") in service_routes:
                expected_schedules.append(ScheduleData.from_dict(schedule))
        service_schedules = mbta_service.get_schedules(stop_id, service_routes)
        
        expected_schedules.sort(key=lambda sched: sched.id)
        service_schedules.sort(key=lambda sched: sched.id)
        
        assert len(service_schedules) == len(expected_schedules)
        for expected, service in zip(expected_schedules, service_schedules):
            assert expected.id == service.id
        
    def test_service_retrieves_correct_trips(self, mock_mbta_client, create_stop_and_route):
        service_routes = mbta_service.get_route_set()
        with open(f"{settings.MOCK_DATA}trips.json", "r") as file:
            data = json.load(file)
        
        expected_trips = []
        for trip in data.get("data"):
            expected_trips.append(TripData.from_dict(trip))
        service_trips = mbta_service.get_trips(service_routes)
            
        expected_trips.sort(key=lambda trip: trip.id)
        service_trips.sort(key=lambda trip: trip.id)
        
        assert len(expected_trips) == len(service_trips)
        for expected, service in zip(expected_trips, service_trips):
            assert expected.id == service.id
        
    def test_service_retrieves_correct_vehicles(self, mock_mbta_client, create_stop_and_route):
        with open(f"{settings.MOCK_DATA}vehicles.json", "r") as file:
            data = json.load(file)
        expected_vehicles = []
        for vehicle in data.get("data"):
            expected_vehicles.append(VehicleData.from_dict(vehicle))
        service_vehicles = mbta_service.get_vehicles()
            
        expected_vehicles.sort(key=lambda veh: veh.id)
        service_vehicles.sort(key=lambda veh: veh.id)
        
        assert len(expected_vehicles) == len(service_vehicles)
        for expected, service in zip(expected_vehicles, service_vehicles):
            assert expected.id == service.id
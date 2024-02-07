from django.utils.functional import SimpleLazyObject

from commuter_rail_departure_core.client import mbta_client
from commuter_rail_departure_departures.models import Route


class MBTAService:
    
    @staticmethod
    def get_route_set(route_type="2"):
        routes = Route.objects.filter(type=route_type)
        return set(routes.values_list("mbta_id", flat=True))

    @staticmethod
    def get_predictions(stop_id, route_set):
        predictions = mbta_client.get_predictions(stop_id=stop_id)
        return [prediction for prediction in predictions if prediction.route_id in route_set]

    @staticmethod
    def get_schedules(stop_id, route_set):
        schedules = mbta_client.get_schedules(stop_id=stop_id)
        return [schedule for schedule in schedules if schedule.route_id in route_set]

    @staticmethod
    def get_trips(route_set):
        return mbta_client.get_trips(route_set)

    @staticmethod
    def get_vehicles(route_type="2"):
        return mbta_client.get_vehicles(route_type)

# avoid uneeded object creation until use
mbta_service = SimpleLazyObject(MBTAService)
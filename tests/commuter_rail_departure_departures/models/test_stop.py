import pytest
import json

from django.conf import settings

from commuter_rail_departure_departures.models import Stop


@pytest.mark.django_db
class TestStop:

    def test_create_stops(self, mock_mbta_client):
        with open(f"{settings.MOCK_DATA}stops.json", "r") as file:
                data = json.load(file)
        num_stops_expected = len(data.get("data"))
        stops = Stop.stops.create_from_mbta_client()
        assert num_stops_expected == len(stops)
        
    def test_get_stations(self, mock_mbta_client):
        with open(f"{settings.MOCK_DATA}stops.json", "r") as file:
                data = json.load(file)
        num_stops_expected = len(data.get("data"))
        stops = Stop.stops.create_from_mbta_client()
        assert num_stops_expected == len(stops)
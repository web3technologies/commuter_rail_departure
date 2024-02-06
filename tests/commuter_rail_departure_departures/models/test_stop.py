import pytest
import json

from django.conf import settings

from commuter_rail_departure_departures.models import Stop


@pytest.mark.django_db
class TestStop:

    def test_create_from_mbta_client(self, mock_mbta_client):
        with open(f"{settings.MOCK_DATA}stops.json", "r") as file:
                data = json.load(file)
        num_stops_expected = len(data.get("data"))
        stops = Stop.stops.create_from_mbta_client()
        assert num_stops_expected == len(stops)
        
    def test_stations(self, mock_mbta_client):
        stops = Stop.stops.create_from_mbta_client()
        station_count = 269
        stops = Stop.stops.stations()
        assert station_count == len(stops)
        
    @pytest.mark.django_db
    def test_with_child_count(self, mock_mbta_client):
        Stop.stops.create_from_mbta_client()
        stations_with_count = Stop.stops.with_child_count()
        for station in stations_with_count:
            assert station.child_stops_count == Stop.objects.filter(parent_station=station).count()

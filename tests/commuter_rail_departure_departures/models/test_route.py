import pytest
import json

from django.conf import settings

from commuter_rail_departure_departures.models import Route


@pytest.mark.django_db
class TestRoute:

    def test_create_from_mbta_client(self, mock_mbta_client):
        with open(f"{settings.MOCK_DATA}routes.json", "r") as file:
                data = json.load(file)
        num_stops_expected = len(data.get("data"))
        routes = Route.routes.create_from_mbta_client()
        assert num_stops_expected == len(routes)

import pytest

from rest_framework.test import APIClient

from commuter_rail_departure_departures.models import Stop
from commuter_rail_departure_departures.serializer.stop import StopSerializer


@pytest.mark.django_db
class TestStopReadOnlyViewset:

    url = "/departures/stop-names/"
    client = APIClient()

    def test_list_stops(self):

        Stop.stops.create_from_mbta_client()
        stops = Stop.stops.with_child_count().order_by("name")
        expected_res = StopSerializer(stops, many=True).data
        response = self.client.get(self.url)
        
        assert response.status_code == 200
        assert response.data == expected_res
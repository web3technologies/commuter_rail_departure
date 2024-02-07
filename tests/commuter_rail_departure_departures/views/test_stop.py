import pytest
import pytz
import datetime
import json
from freezegun import freeze_time

from django.conf import settings
from rest_framework.test import APIClient

from commuter_rail_departure_departures.models import Stop
from commuter_rail_departure_departures.serializer.stop import StopSerializer


@pytest.mark.django_db
class TestStopReadOnlyViewset:

    url = "/departures/stop/"
    client = APIClient()

    def test_list_stops(self, create_stop_and_route):

        stops = Stop.stops.with_child_count().order_by("name")
        expected_res = StopSerializer(stops, many=True).data
        response = self.client.get(self.url)
        
        assert response.status_code == 200
        assert response.data == expected_res
    
    def test_retrieve_departure_arrival_data(self, mock_mbta_client, create_stop_and_route):
        with open(f"{settings.TEST_DATA}arrival_data.json", "r") as file:
            expected_res_data = json.load(file)
        stop = Stop.objects.get(mbta_id="place-north")
        moved_time = "2024-02-06 06:44:00"
        eastern = pytz.timezone('US/Eastern')
        moved_time_dt = eastern.localize(datetime.datetime.strptime(moved_time, "%Y-%m-%d %H:%M:%S"))
        with freeze_time(moved_time_dt) as freezer:
            res = self.client.get(f"{self.url}{stop.mbta_id}/")
            
        assert res.status_code == 200
        assert res.data == expected_res_data
        
    def test_retrieve_departure_arrival_data_skips_passed_time(self, mock_mbta_client, create_stop_and_route):
        """If the current time is passed the schedule departure time we dont want to retrieve the records"""
        stop = Stop.objects.get(mbta_id="place-north")
        moved_time = "2024-02-10 06:44:00"
        eastern = pytz.timezone('US/Eastern')
        moved_time_dt = eastern.localize(datetime.datetime.strptime(moved_time, "%Y-%m-%d %H:%M:%S"))
        with freeze_time(moved_time_dt) as freezer:
            res = self.client.get(f"{self.url}{stop.mbta_id}/")
            
        assert res.status_code == 200
        assert res.data.get("departures") == []
        
        
    def test_retrieve_stop_does_not_exist(self, mock_mbta_client):
        res = self.client.get(f"{self.url}invalid-mbta-id/")
        assert res.status_code == 404
import pytest
from rest_framework.test import APIClient
import pytz
import datetime
from django.contrib.auth import get_user_model
from freezegun import freeze_time

from commuter_rail_departure_departures.models import Stop, Route


@pytest.mark.django_db
class TestDeparturesApiView:

    url = "/departures/api/"
    client = APIClient()
    
    def test_list_departures(self, 
        mock_mbta_client
    ):
        Stop.stops.create_from_mbta_client()
        Route.routes.create_from_mbta_client()
        
        expected_data = [['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:07 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:44:21 AM', 'South Station', '1829', 'LATE'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:45:45 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:00 AM', 'South Station', '1709', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:47:16 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME'],
                        ['MBTA', '09:50:03 AM', 'South Station', '1829', 'ON-TIME']]
        
        moved_time = "2024-02-06 09:44:00"
        eastern = pytz.timezone('US/Eastern')
        moved_time_dt = eastern.localize(datetime.datetime.strptime(moved_time, "%Y-%m-%d %H:%M:%S"))
        with freeze_time(moved_time_dt) as freezer:
            res = self.client.get(self.url)            
            assert res.data.get("eastern_date") == "2024-02-06"
            assert res.data.get("eastern_time") == "09:44:00 AM"
        
        
        
        
        
from datetime import datetime
import pytest
import pytz
from freezegun import freeze_time
import json

from django.conf import settings

from commuter_rail_departure_departures.models import Stop, Route
from commuter_rail_departure_departures.processor.departure_processor import DepartureProcessor


@pytest.mark.django_db
class TestDepartureProcessor:
    
    def test_processor_gets_good_data(self, mock_mbta_client):
        Stop.stops.create_from_mbta_client()
        Route.routes.create_from_mbta_client()
        stop = Stop.objects.get(mbta_id="place-sstat")
        moved_time = "2024-02-06 06:44:00"
        eastern = pytz.timezone('US/Eastern')
        moved_time_dt = eastern.localize(datetime.strptime(moved_time, "%Y-%m-%d %H:%M:%S"))
        with open(f"{settings.TEST_DATA}departure_data1.json", "r") as file:
            expected_res_data = json.load(file)
        with freeze_time(moved_time_dt) as freezer:
            eastern_time = datetime.now(eastern)
            data = DepartureProcessor.process_data(stop.mbta_id, eastern_time)
        assert data == expected_res_data
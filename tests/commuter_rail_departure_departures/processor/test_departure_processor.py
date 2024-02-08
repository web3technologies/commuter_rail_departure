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
    
    def test_processor_gets_good_data(self, mock_mbta_client, create_stop_and_route):
        """Esnure the data produced by the processor is as expected"""
        stop = Stop.objects.get(mbta_id="place-sstat")
        moved_time = "2024-02-06 06:44:00"
        eastern = pytz.timezone('US/Eastern')
        moved_time_dt = eastern.localize(datetime.strptime(moved_time, "%Y-%m-%d %H:%M:%S"))
        with open(f"{settings.TEST_DATA}departure_data.json", "r") as file:
            expected_departure_data = json.load(file)
        with open(f"{settings.TEST_DATA}arrival_data.json", "r") as file:
            expected_arrival_data = json.load(file)
        with freeze_time(moved_time_dt) as freezer:
            eastern_time = datetime.now(eastern)
            processor = DepartureProcessor(stop.mbta_id, eastern_time)
            departure_data, arrival_data = processor.process_data()
        assert departure_data == expected_departure_data
        assert arrival_data == expected_arrival_data
        
    def test_processor_receives_invalid_mbta_id(self, mock_mbta_client, create_stop_and_route):
        """Ensure that if a bad id is passed and empty list will be returned"""
        mbta_id="bad id"
        moved_time = "2024-02-06 06:44:00"
        eastern = pytz.timezone('US/Eastern')
        moved_time_dt = eastern.localize(datetime.strptime(moved_time, "%Y-%m-%d %H:%M:%S"))
        with freeze_time(moved_time_dt) as freezer:
            eastern_time = datetime.now(eastern)
            processor = DepartureProcessor(mbta_id, eastern_time)
            departure_data, arrival_data = processor.process_data()
        assert departure_data == []
        assert arrival_data == []
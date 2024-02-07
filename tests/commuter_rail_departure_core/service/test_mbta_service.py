from datetime import datetime
import pytest
import pytz
from freezegun import freeze_time


from commuter_rail_departure_core.service import mbta_service


@pytest.mark.django_db
class TestMbtaService:
    
    def test_service_retrieves_correct_routes(self, mock_mbta_client, create_stop_and_route):
        ...
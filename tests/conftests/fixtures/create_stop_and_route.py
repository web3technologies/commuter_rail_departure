import pytest

from commuter_rail_departure_departures.models import Route, Stop


@pytest.fixture(scope="function")
def create_stop_and_route():
    Stop.stops.create_from_mbta_client()
    Route.routes.create_from_mbta_client()
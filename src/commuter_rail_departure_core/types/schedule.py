from datetime import datetime

from commuter_rail_departure_core.types.format_date_mixin import FormatDateMixin

class ScheduleData(FormatDateMixin):
    def __init__(self, 
                 arrival_time: datetime, 
                 departure_time: datetime, 
                 direction_id: int, 
                 drop_off_type: int, 
                 pickup_type: int, 
                 stop_headsign: str, 
                 stop_sequence: int, 
                 timepoint: bool, 
                 id: str, 
                 route_id: str, 
                 stop_id: str, 
                 trip_id: str):
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.direction_id = direction_id
        self.drop_off_type = drop_off_type
        self.pickup_type = pickup_type
        self.stop_headsign = stop_headsign
        self.stop_sequence = stop_sequence
        self.timepoint = timepoint
        self.id = id
        self.route_id = route_id
        self.stop_id = stop_id
        self.trip_id = trip_id

    @classmethod
    def from_dict(cls, data: dict):
        attributes = data['attributes']
        relationships = data['relationships']
        return cls(
            arrival_time=cls.format_date(attributes.get('arrival_time')),
            departure_time=cls.format_date(attributes.get('departure_time')),
            direction_id=attributes.get('direction_id'),
            drop_off_type=attributes.get('drop_off_type'),
            pickup_type=attributes.get('pickup_type'),
            stop_headsign=attributes.get('stop_headsign'),
            stop_sequence=attributes.get('stop_sequence'),
            timepoint=attributes.get('timepoint'),
            id=data.get('id'),
            route_id=relationships['route']['data']['id'],
            stop_id=relationships['stop']['data']['id'],
            trip_id=relationships['trip']['data']['id']
        )

    def __repr__(self) -> str:
        return f"Schedule(id='{self.id}', route_id='{self.route_id}', trip_id='{self.trip_id}', stop_id='{self.stop_id}', departure_time='{self.departure_time}')"

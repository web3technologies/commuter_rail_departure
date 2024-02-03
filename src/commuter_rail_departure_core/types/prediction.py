from commuter_rail_departure_core.types.format_date_mixin import FormatDateMixin


class PredictionData(FormatDateMixin):
    
    def __init__(self, 
                 arrival_time: str, 
                 arrival_uncertainty: bool, 
                 departure_time: str, 
                 departure_uncertainty: bool, 
                 direction_id: int, 
                 revenue: str, 
                 schedule_relationship: bool, 
                 status: bool, 
                 stop_sequence: int,
                 id: str,
                 route_id: str,
                 stop_id: str,
                 trip_id: str,
                 vehicle_id: str
        ):
            self.arrival_time = self.format_date(arrival_time)
            self.arrival_uncertainty = arrival_uncertainty
            self.departure_time = self.format_date(departure_time)
            self.departure_uncertainty = departure_uncertainty
            self.direction_id = direction_id
            self.revenue = revenue
            self.schedule_relationship = schedule_relationship
            self.status = status
            self.stop_sequence = stop_sequence
            self.id = id
            self.route_id = route_id
            self.stop_id = stop_id
            self.trip_id = trip_id
            self.vehicle_id = vehicle_id
    
    @property    
    def arrival_time_str(self):
        if self.arrival_time:
            return self.arrival_time.strftime("%Y-%m-%d %I:%M:%S")
        return self.arrival_time
    
    @property    
    def departure_time_str(self):
        if self.departure_time:
            return self.departure_time.strftime("%Y-%m-%d %I:%M:%S")
        return self.departure_time

    @classmethod
    def from_dict(cls, data: dict):
        attributes = data['attributes']
        relationships = data['relationships']
        return cls(
            arrival_time=attributes.get('arrival_time'),
            arrival_uncertainty=attributes.get('arrival_uncertainty', False),
            departure_time=attributes.get('departure_time'),
            departure_uncertainty=attributes.get('departure_uncertainty', False),
            direction_id=attributes.get('direction_id'),
            revenue=attributes.get('revenue'),
            schedule_relationship=attributes.get('schedule_relationship', False),
            status=attributes.get('status', False),
            stop_sequence=attributes.get('stop_sequence'),
            id=data.get('id'),
            route_id=relationships['route']['data']['id'],
            stop_id=relationships['stop']['data']['id'],
            trip_id=relationships['trip']['data']['id'],
            vehicle_id=relationships['vehicle']['data'].get('id') if relationships['vehicle'].get("data") else None
        )

    def __repr__(self) -> str:
        return f"Prediction(id='{self.id}', arrival_time='{self.arrival_time}', departure_time='{self.departure_time}', route_id='{self.route_id}', trip_id='{self.trip_id}', vehicle_id='{self.vehicle_id}')"

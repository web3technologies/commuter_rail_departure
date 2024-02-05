from typing import List, Optional

class Carriage:
    
    def __init__(self, label: str, occupancy_percentage: Optional[int], occupancy_status: str):
        self.label = label
        self.occupancy_percentage = occupancy_percentage
        self.occupancy_status = occupancy_status

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            label=data.get('label'),
            occupancy_percentage=data.get('occupancy_percentage'),
            occupancy_status=data.get('occupancy_status')
        )

class VehicleData:
    
    def __init__(self, 
                 id: str, 
                 bearing: int, 
                 carriages: List[Carriage], 
                 current_status: str, 
                 current_stop_sequence: int, 
                 direction_id: int, 
                 label: str, 
                 latitude: float, 
                 longitude: float, 
                 occupancy_status: Optional[str], 
                 revenue: str, 
                 speed: Optional[float], 
                 updated_at: str, 
                 route_id: str, 
                 stop_id: str, 
                 trip_id: str):
        self.id = id
        self.bearing = bearing
        self.carriages = carriages
        self.current_status = current_status
        self.current_stop_sequence = current_stop_sequence
        self.direction_id = direction_id
        self.label = label
        self.latitude = latitude
        self.longitude = longitude
        self.occupancy_status = occupancy_status
        self.revenue = revenue
        self.speed = speed
        self.updated_at = updated_at
        self.route_id = route_id
        self.stop_id = stop_id
        self.trip_id = trip_id

    @classmethod
    def from_dict(cls, data: dict):
        attributes = data['attributes']
        relationships = data['relationships']
        carriages = [Carriage.from_dict(carriage) for carriage in attributes.get('carriages', [])]
        print()
        return cls(
            id=data.get('id'),
            bearing=attributes.get('bearing'),
            carriages=carriages,
            current_status=attributes.get('current_status'),
            current_stop_sequence=attributes.get('current_stop_sequence'),
            direction_id=attributes.get('direction_id'),
            label=attributes.get('label'),
            latitude=attributes.get('latitude'),
            longitude=attributes.get('longitude'),
            occupancy_status=attributes.get('occupancy_status'),
            revenue=attributes.get('revenue'),
            speed=attributes.get('speed'),
            updated_at=attributes.get('updated_at'),
            route_id=relationships['route']['data']['id'],
            stop_id=relationships['stop']['data']['id'] if relationships["stop"].get("data") else "",
            trip_id=relationships['trip']['data']['id'] if relationships["trip"].get("data") else ""
        )

    def __repr__(self) -> str:
        return f"Vehicle(id='{self.id}', label='{self.label}', current_status='{self.current_status}', route_id='{self.route_id}', trip_id='{self.trip_id}')"

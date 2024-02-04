class TripData:
    
    def __init__(self, 
                 id: str, 
                 bikes_allowed: int, 
                 block_id: str, 
                 direction_id: int, 
                 headsign: str, 
                 name: str, 
                 revenue: str, 
                 wheelchair_accessible: int, 
                 route_id: str, 
                 route_pattern_id: str, 
                 service_id: str, 
                 shape_id: str):
        self.id = id
        self.bikes_allowed = bikes_allowed
        self.block_id = block_id
        self.direction_id = direction_id
        self.headsign = headsign
        self.name = name
        self.revenue = revenue
        self.wheelchair_accessible = wheelchair_accessible
        self.route_id = route_id
        self.route_pattern_id = route_pattern_id
        self.service_id = service_id
        self.shape_id = shape_id

    @classmethod
    def from_dict(cls, data: dict):
        attributes = data['attributes']
        relationships = data['relationships']
        return cls(
            id=data.get('id'),
            bikes_allowed=attributes.get('bikes_allowed'),
            block_id=attributes.get('block_id'),
            direction_id=attributes.get('direction_id'),
            headsign=attributes.get('headsign'),
            name=attributes.get('name'),
            revenue=attributes.get('revenue'),
            wheelchair_accessible=attributes.get('wheelchair_accessible'),
            route_id=relationships['route']['data'].get('id'),
            route_pattern_id=relationships['route_pattern']['data'].get('id'),
            service_id=relationships['service']['data'].get('id') if relationships['service']['data'] else None,
            shape_id=relationships['shape']['data'].get('id')
        )

    def __repr__(self) -> str:
        return f"Trip(id='{self.id}', headsign='{self.headsign}', route_id='{self.route_id}')"

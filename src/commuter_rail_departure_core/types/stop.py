class StopData:
    
    def __init__(self, 
                 id: str, 
                 address: str, 
                 latitude: float, 
                 longitude: float, 
                 municipality: str, 
                 name: str, 
                 location_type: int, 
                 wheelchair_boarding: int, 
                 at_street: str = None,
                 description: str = None,
                 on_street: str = None,
                 platform_code: str = None,
                 platform_name: str = None,
                 vehicle_type: int = None,
                 zone_id: str = None,
                 parent_station_id: str = None):
        self.id = id
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.municipality = municipality
        self.name = name
        self.location_type = location_type
        self.wheelchair_boarding = wheelchair_boarding
        self.at_street = at_street
        self.description = description
        self.on_street = on_street
        self.platform_code = platform_code
        self.platform_name = platform_name
        self.vehicle_type = vehicle_type
        self.zone_id = zone_id
        self.parent_station_id = parent_station_id

    @classmethod
    def from_dict(cls, data: dict):
        attributes = data['attributes']
        relationships = data['relationships']
        zone_data = relationships.get('zone', {}).get('data')
        parent_station_data = relationships.get('parent_station', {}).get('data')
        return cls(
            id=data.get('id'),
            address=attributes.get('address'),
            latitude=attributes.get('latitude'),
            longitude=attributes.get('longitude'),
            municipality=attributes.get('municipality'),
            name=attributes.get('name'),
            location_type=attributes.get('location_type'),
            wheelchair_boarding=attributes.get('wheelchair_boarding'),
            at_street=attributes.get('at_street'),
            description=attributes.get('description'),
            on_street=attributes.get('on_street'),
            platform_code=attributes.get('platform_code'),
            platform_name=attributes.get('platform_name'),
            vehicle_type=attributes.get('vehicle_type'),
            zone_id=zone_data.get('id') if zone_data else None,
            parent_station_id=parent_station_data.get('id') if parent_station_data else None
        )

    def __repr__(self) -> str:
        return f"StopData(id='{self.id}', name='{self.name}', address='{self.address}', municipality='{self.municipality}', zone_id='{self.zone_id}', parent_station_id='{self.parent_station_id}')"

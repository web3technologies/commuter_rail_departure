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
                 zone_id: str = None):
        self.id = id
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.municipality = municipality
        self.name = name
        self.location_type = location_type
        self.wheelchair_boarding = wheelchair_boarding
        self.zone_id = zone_id

    @classmethod
    def from_dict(cls, data: dict):
        attributes = data['attributes']
        zone_data = data['relationships']['zone']['data']
        zone_id = zone_data['id'] if zone_data else None
        return cls(
            id=data.get('id'),
            address=attributes.get('address'),
            latitude=attributes.get('latitude'),
            longitude=attributes.get('longitude'),
            municipality=attributes.get('municipality'),
            name=attributes.get('name'),
            location_type=attributes.get('location_type'),
            wheelchair_boarding=attributes.get('wheelchair_boarding'),
            zone_id=zone_id
        )

    def __repr__(self) -> str:
        return f"Stop(id='{self.id}', name='{self.name}', address='{self.address}', municipality='{self.municipality}', zone_id='{self.zone_id}')"

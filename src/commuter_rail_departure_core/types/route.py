from typing import List


class RouteData:
    
    def __init__(self, id: str, type: int, color: str, description: str, direction_destinations: List[str], direction_names: List[str], fare_class: str, long_name: str, short_name: str, sort_order: int, text_color: str, line_id: str) -> None:
        self.id = id
        self.type = type
        self.color = color
        self.description = description
        self.direction_destinations = direction_destinations
        self.direction_names = direction_names
        self.fare_class = fare_class
        self.long_name = long_name
        self.short_name = short_name
        self.sort_order = sort_order
        self.text_color = text_color
        self.line_id = line_id

    @classmethod
    def from_dict(cls, data: dict):
        attributes = data['attributes']
        relationships = data['relationships']
        return cls(
            id=data['id'],
            type=attributes['type'],
            color=attributes['color'],
            description=attributes['description'],
            direction_destinations=attributes['direction_destinations'],
            direction_names=attributes['direction_names'],
            fare_class=attributes['fare_class'],
            long_name=attributes['long_name'],
            short_name=attributes['short_name'],
            sort_order=attributes['sort_order'],
            text_color=attributes['text_color'],
            line_id=relationships['line']['data']['id']
        )
        
    def __str__(self) -> str:
        return self.long_name
    
    def __repr__(self) -> str:
        return f"Route(id='{self.id}', type={self.type}, long_name='{self.long_name}', color='{self.color}')"

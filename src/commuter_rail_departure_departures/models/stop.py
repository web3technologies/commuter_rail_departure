from django.db import models

from commuter_rail_departure_core.client import mbta_client


class StopManager(models.Manager):
    
    def create_from_mbta_client(self) -> list:
        all_stops = []
        stops = mbta_client.get_stops()
        parent_stations = [
            self.model(
               mbta_id=stop.id,
               address=stop.address,
               latitude=stop.latitude,
               longitude=stop.longitude,
               municipality=stop.municipality,
               name=stop.name,
               location_type=stop.location_type,
                wheelchair_boarding=stop.wheelchair_boarding,
                at_street=stop.at_street,
                description=stop.description,
                on_street=stop.on_street,
                platform_code=stop.platform_code,  
                platform_name=stop.platform_name,
                vehicle_type=stop.vehicle_type,
                zone_id=stop.zone_id,
                parent_station=None
            )
            for stop in [stop for stop in stops if stop.parent_station_id is None]
        ]
        all_stops.extend(self.bulk_create(parent_stations, ignore_conflicts=True))
        parent_station_cache = {}
        child_stops = []
        for stop in stops:
            if stop.parent_station_id is not None:
                if stop.parent_station_id not in parent_station_cache:
                    parent_station_cache[stop.parent_station_id] = self.get(mbta_id=stop.parent_station_id)
                parent_station = parent_station_cache[stop.parent_station_id]
                child_stop = self.model(
                    mbta_id=stop.id,
                    address=stop.address,
                    latitude=stop.latitude,
                    longitude=stop.longitude,
                    municipality=stop.municipality,
                    name=stop.name,
                    location_type=stop.location_type,
                    wheelchair_boarding=stop.wheelchair_boarding,
                    at_street=stop.at_street,
                    description=stop.description,
                    on_street=stop.on_street,
                    platform_code=stop.platform_code,  
                    platform_name=stop.platform_name,
                    vehicle_type=stop.vehicle_type,
                    zone_id=stop.zone_id,
                    parent_station=parent_station
                )
                child_stops.append(child_stop)
        all_stops.extend(self.bulk_create(child_stops, ignore_conflicts=True))
        return all_stops
    
    def with_child_count(self):
        return self.stations().annotate(child_stops_count=models.Count("child_stops"))
    
    def stations(self):
        """ Returns a list of all stations

        Returns:
            _type_: _description_
        """
        return self.filter(parent_station__isnull=True, location_type=1)

class Stop(models.Model):
    
    mbta_id = models.CharField(max_length=255, unique=True)     # can be text or digit from api
    address = models.CharField(max_length=255, null=True, default=None)
    latitude = models.FloatField(null=True, default=None)
    longitude = models.FloatField(null=True, default=None)
    municipality = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    location_type = models.IntegerField()
    wheelchair_boarding = models.IntegerField()
    at_street = models.CharField(max_length=255, null=True, default=None)
    description = models.TextField(null=True, default=None)
    on_street = models.CharField(max_length=255, null=True, default=None)    
    platform_code = models.CharField(max_length=255, null=True, default=None)    
    platform_name = models.CharField(max_length=255, null=True, default=None)    
    vehicle_type = models.IntegerField(null=True, default=None)    
    zone_id = models.CharField(max_length=255, null=True, default=None)
    parent_station = models.ForeignKey(
        "Stop", 
        null=True, 
        default=None, 
        on_delete=models.CASCADE, 
        related_name="child_stops"
    )
    
    objects = models.Manager()
    stops = StopManager()
    
    
    def __str__(self) -> str:
        return self.name
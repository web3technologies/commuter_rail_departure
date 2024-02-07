from typing import List, Optional

from django.db import models
from django.contrib.postgres.fields import ArrayField

from commuter_rail_departure_core.client import mbta_client


class RouteManager(models.Manager):
    
    def create_from_mbta_client(self, types:Optional[List[str]] = ["2"]) -> list:
        all_routes = []
        ## better as a param but default for requirements
        routes = mbta_client.get_routes(types=types)
        for route in routes:
            all_routes.append(
                Route(
                   mbta_id=route.id,
                   type=route.type,
                   color=route.color,
                   description=route.description,
                   direction_destinations=route.direction_destinations,
                   direction_names=route.direction_names,
                   fare_class=route.fare_class,
                   long_name=route.long_name,
                   short_name=route.short_name,
                   sort_order=route.sort_order,
                   text_color=route.text_color,
                   line_id=route.line_id
                )
            )
        return self.bulk_create(all_routes, ignore_conflicts=True)
            

        
class Route(models.Model):

    mbta_id = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    description = models.TextField()
    direction_destinations = ArrayField(models.CharField(max_length=100), default=list)
    direction_names = ArrayField(models.CharField(max_length=100), default=list)
    fare_class = models.CharField(max_length=25)
    long_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=25)
    sort_order = models.IntegerField()
    text_color = models.CharField(max_length=25)
    line_id = models.CharField(max_length=25)
    
    objects = models.Manager()
    routes = RouteManager()
    
    def __str__(self) -> str:
        return self.mbta_id
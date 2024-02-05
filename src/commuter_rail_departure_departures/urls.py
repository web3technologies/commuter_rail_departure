from django.urls import path
from commuter_rail_departure_departures.views import *

urlpatterns = [
    path('test', DeparturesView.as_view(), name='template-departures'),
    path("api", DeparturesApiView.as_view())
]
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("departures/", include("commuter_rail_departure_departures.urls"))
]

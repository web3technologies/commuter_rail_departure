from rest_framework.serializers import ModelSerializer
from commuter_rail_departure_departures.models import Stop



class StopSerializer(ModelSerializer):

    class Meta:
        model = Stop
        fields = ["name", "mbta_id"]
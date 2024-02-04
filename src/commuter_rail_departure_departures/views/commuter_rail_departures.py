from datetime import datetime
import pytz

from django.views.generic import TemplateView

from commuter_rail_departure_departures.test_data import get_data


class DeparturesView(TemplateView):
    template_name = 'commuter_rail_departure_departures/departures.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eastern = pytz.timezone('US/Eastern')
        eastern_time = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S")
        context['departures'] = get_data()
        context["eastern_time"] = eastern_time
        return context

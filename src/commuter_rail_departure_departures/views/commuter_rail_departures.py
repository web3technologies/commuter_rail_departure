from django.views.generic import TemplateView
from commuter_rail_departure_departures.test_data import get_data


class DeparturesView(TemplateView):
    template_name = 'commuter_rail_departure_departures/departures.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departures'] = get_data()
        return context

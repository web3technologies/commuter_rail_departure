from rest_framework.views import ApiView



class ArrivalApi(APiView):

    def get(self, request):
        "https://api-v3.mbta.com/routes?filter%5Bstop%5D=place-north&filter[type]=2`"
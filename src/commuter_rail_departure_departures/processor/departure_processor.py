from datetime import timedelta

from commuter_rail_departure_core.service import mbta_service
from commuter_rail_departure_departures.models import Stop


class DepartureProcessor:
    
    def __init__(self, mbta_id:str, eastern_time):
        self.__mbta_id = mbta_id
        self.__departure_data = []
        self.__arival_only_data = []
        self.__eastern_time = eastern_time
    
    @property
    def arrival_data(self):
        return self.__arival_only_data
    
    @property
    def departure_data(self):
        return self.__departure_data

        
    def __retrieve_data_set(self):
        """Using the MBTA service retrieve all of the data that should be expected"""
        route_set = mbta_service.get_route_set()
        predictions = mbta_service.get_predictions(self.__mbta_id, route_set)
        schedules = mbta_service.get_schedules(self.__mbta_id, route_set)
        trips = mbta_service.get_trips(route_set)
        vehicles = mbta_service.get_vehicles()
        return route_set, predictions, schedules, trips, vehicles
    
    def __create_workable_data(self, route_set, predictions, schedules, trips, vehicles):
        """Using the data from the MBTA service create the data structures that will be used by the serializer to generate the departure data"""
        trip_id_to_prediction_mapping = {(prediction.trip_id, prediction.stop_id): prediction for prediction in predictions if prediction.route_id in route_set}
        trip_id_to_schedule_mapping = {(schedule.trip_id, schedule.stop_id): schedule for schedule in schedules if schedule.route_id in route_set} 
        trip_cache = {trip.id:trip for trip in trips}
        trip_id_to_vehicle_mapping = {vehicle.trip_id: vehicle for vehicle in vehicles}
        
        return trip_id_to_prediction_mapping, trip_id_to_schedule_mapping, trip_cache, trip_id_to_vehicle_mapping
    
    def __get_status(self, predicted_time, scheduled_time):
        """ Determine the status based on the prediction"""
        if predicted_time and scheduled_time:
            time_diff = predicted_time - scheduled_time
            if time_diff < timedelta(minutes=0):
                status = "EARLY"
            elif time_diff >= timedelta(minutes=0) and time_diff < timedelta(minutes=3):
                status = "ON-TIME"
            else:
                status = "LATE"
        else:
            status = None
        return status
    
    def __serializer_added_predictions(self, predictions, route_set, trip_cache, trip_id_to_vehicle_mapping):
        """
            Handle added predictions that are not in the schedule dataset. 
            They will not be found in the schedule mapping because they are added after the schedule has been made by the mbta system
        """
        for prediction in predictions:
            if (
                prediction.route_id in route_set and 
                prediction.schedule_relationship == "ADDED" and
                prediction.departure_time < self.__eastern_time
            ):
                self.__departure_data.append(
                    {
                        "carrier": "MBTA",
                        "departure_time": str(prediction.departure_time) if prediction.departure_time else None,
                        "destination": trip_cache[prediction.trip_id].headsign if prediction.trip_id in trip_cache else None, 
                        "vehicle_id": trip_id_to_vehicle_mapping[prediction.trip_id].label if prediction.trip_id in trip_id_to_vehicle_mapping else None, 
                        "status": "ADDED",
                        "has_prediction": False
                    }
                )
                
                
    def __handle_arival(self,schedule, trip_id_to_prediction_mapping, trip_id_to_vehicle_mapping):
        if self.__eastern_time > schedule.arrival_time:
            return
        if (schedule.trip_id, schedule.stop_id) in trip_id_to_prediction_mapping:
            prediction = trip_id_to_prediction_mapping[(schedule.trip_id, schedule.stop_id)]
            if self.__eastern_time > prediction.arrival_time:
                return
            status = self.__get_status(prediction.arrival_time, schedule.arrival_time)
            arrival = (
                {
                    "carrier": "MBTA",
                    "arrival_time": str(prediction.arrival_time) if prediction.arrival_time else prediction.stop_sequence,
                    "destination": Stop.objects.get(mbta_id=trip_id_to_vehicle_mapping[prediction.trip_id].stop_id).name if prediction.trip_id in trip_id_to_vehicle_mapping else None, 
                    "vehicle_id": trip_id_to_vehicle_mapping[prediction.trip_id].label if prediction.trip_id in trip_id_to_vehicle_mapping else "TBD", 
                    "status": prediction.schedule_relationship if prediction.schedule_relationship == "ADDED" else status,
                }
            )
        else:
            arrival = (
                {
                    "carrier": "MBTA",
                    "arrival_time": str(schedule.arrival_time) if schedule.arrival_time else schedule.stop_sequence,
                    "destination": Stop.objects.get(mbta_id=trip_id_to_vehicle_mapping[schedule.trip_id].stop_id).name if schedule.trip_id in trip_id_to_vehicle_mapping else None, 
                    "vehicle_id": trip_id_to_vehicle_mapping[schedule.trip_id].label if schedule.trip_id in trip_id_to_vehicle_mapping else "TBD", 
                    "status": "ON-TIME",
                }
            )
        self.__arival_only_data.append(arrival)
        
    def __handle_departure(self, schedule, trip_id_to_prediction_mapping, trip_cache, trip_id_to_vehicle_mapping):
        # if current eastern time > the departure time no need to display the data
        if self.__eastern_time > schedule.departure_time:
            return
        # this signals a prediction has been found for the schedule
        elif (schedule.trip_id, schedule.stop_id) in trip_id_to_prediction_mapping:
            prediction = trip_id_to_prediction_mapping[(schedule.trip_id, schedule.stop_id)]
            status = self.__get_status(prediction.departure_time, schedule.departure_time)
            departure = (
                {
                    "carrier": "MBTA",
                    "departure_time": str(prediction.departure_time) if prediction.departure_time else None,
                    "destination": trip_cache[prediction.trip_id].headsign if prediction.trip_id in trip_cache else None, 
                    "vehicle_id": trip_id_to_vehicle_mapping[prediction.trip_id].label if prediction.trip_id in trip_id_to_vehicle_mapping else "TBD", 
                    "status": prediction.schedule_relationship if prediction.schedule_relationship == "ADDED" else status,
                }
            )
        # if there is no prediction available then display the scheduled departure
        else:
            departure = (
                {
                    "carrier": "MBTA",
                    "departure_time": str(schedule.departure_time) if schedule.departure_time else None,
                    "destination": trip_cache[schedule.trip_id].headsign if schedule.trip_id in trip_cache else None, 
                    "vehicle_id": trip_id_to_vehicle_mapping[schedule.trip_id].label if schedule.trip_id in trip_id_to_vehicle_mapping else "TBD", 
                    "status": "ON-TIME",
                }
            )
        self.__departure_data.append(departure)

    def __serialize_dataset(self, trip_id_to_prediction_mapping, trip_id_to_schedule_mapping, trip_cache, trip_id_to_vehicle_mapping):
        """Using the data from the workable data serialize the data so it available to send via the api"""
        for _, schedule in trip_id_to_schedule_mapping.items():
            # if no departure time documentation states this should be treated as a last stop arrival
            if not schedule.departure_time:
                self.__handle_arival(schedule, trip_id_to_prediction_mapping, trip_id_to_vehicle_mapping)
            else:
                self.__handle_departure(schedule, trip_id_to_prediction_mapping, trip_cache, trip_id_to_vehicle_mapping)
                
    
    def process_data(self):
        """ Entry method that is the global process to return the data"""
        route_set, predictions, schedules, trips, vehicles = self.__retrieve_data_set()
        trip_id_to_prediction_mapping, trip_id_to_schedule_mapping, trip_cache, trip_id_to_vehicle_mapping = self.__create_workable_data(
            route_set, 
            predictions, 
            schedules, 
            trips, 
            vehicles
        )
        self.__serialize_dataset(trip_id_to_prediction_mapping, trip_id_to_schedule_mapping, trip_cache, trip_id_to_vehicle_mapping)
        self.__serializer_added_predictions(predictions, route_set, trip_cache, trip_id_to_vehicle_mapping)
        self.__departure_data.sort(key=lambda predictionData: (predictionData["departure_time"]))
        self.__arival_only_data.sort(key=lambda arrivalData: arrivalData["arrival_time"])
        return self.__departure_data, self.__arival_only_data
    
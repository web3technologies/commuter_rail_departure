from datetime import timedelta

from commuter_rail_departure_core.service import mbta_service



class DepartureProcessor:
    
    @staticmethod
    def process_data(mbta_id, eastern_time):
    
        route_set = mbta_service.get_route_set()
        predictions = mbta_service.get_predictions(mbta_id, route_set)
        schedules = mbta_service.get_schedules(mbta_id, route_set)
        trips = mbta_service.get_trips(route_set)
        vehicles = mbta_service.get_vehicles()
            
        data = []
        trip_id_to_prediction_mapping = {(prediction.trip_id, prediction.stop_id): prediction for prediction in predictions if prediction.route_id in route_set}
        trip_id_to_schedule_mapping = {(schedule.trip_id, schedule.stop_id): schedule for schedule in schedules if schedule.route_id in route_set} 
        trip_cache = {trip.id:trip for trip in trips}
        trip_id_to_vehicle_mapping = {vehicle.trip_id: vehicle for vehicle in vehicles}
        
        for _, schedule in trip_id_to_schedule_mapping.items():
            if not schedule.departure_time or eastern_time > schedule.departure_time:
                continue
            if (schedule.trip_id, schedule.stop_id) in trip_id_to_prediction_mapping:
                prediction = trip_id_to_prediction_mapping[(schedule.trip_id, schedule.stop_id)]
                if prediction.departure_time:
                    time_diff = prediction.departure_time - schedule.departure_time
                    if time_diff < timedelta(minutes=0):
                        status = "EARLY"
                    elif time_diff >= timedelta(minutes=0) and time_diff < timedelta(minutes=3):
                        status = "ON-TIME"
                    else:
                        status = "LATE"
                else:
                    status = "unkown"
                
                append_data = \
                    {
                        "carrier": "MBTA",
                        "departure_time": str(prediction.departure_time) if prediction.departure_time else None,
                        "arrival_time": str(prediction.arrival_time) if prediction.arrival_time else None,
                        "destination": trip_cache[prediction.trip_id].headsign if prediction.trip_id in trip_cache else None, 
                        "vehicle_id": trip_id_to_vehicle_mapping[prediction.trip_id].label if prediction.trip_id in trip_id_to_vehicle_mapping else None, 
                        "status": prediction.schedule_relationship if prediction.schedule_relationship == "ADDED" else status,
                        "has_prediction": True
                    }
            elif not schedule.departure_time:
                status = "FINAL-STOP"
            else:
                status = "ON-TIME"
                append_data = \
                {
                        "carrier": "MBTA",
                        "departure_time": str(schedule.departure_time) if schedule.departure_time else None,
                        "arrival_time": str(schedule.arrival_time) if schedule.arrival_time else None,
                        "destination": trip_cache[schedule.trip_id].headsign if schedule.trip_id in trip_cache else None, 
                        "vehicle_id": trip_id_to_vehicle_mapping[schedule.trip_id].label if schedule.trip_id in trip_id_to_vehicle_mapping else None, 
                        "status": status,
                        "has_prediction": False
                    }
            data.append(append_data)
        data.sort(key=lambda predictionData: (predictionData["departure_time"]))
        
        return data
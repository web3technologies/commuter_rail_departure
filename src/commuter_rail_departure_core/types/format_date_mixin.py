from datetime import datetime
import pytz

class FormatDateMixin:
    @staticmethod
    def format_date(date_str: str):
        if not date_str:
            return None
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        eastern = pytz.timezone('US/Eastern')
        date_obj = date_obj.astimezone(eastern)
        return date_obj
    
    @property    
    def arrival_time_str(self):
        if self.arrival_time:
            return self.arrival_time.strftime("%I:%M:%S %p")
        return self.arrival_time
    
    @property    
    def departure_time_str(self):
        if self.departure_time:
            return self.departure_time.strftime("%I:%M:%S %p")
        return self.departure_time
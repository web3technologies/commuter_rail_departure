from datetime import datetime
import pytz

class FormatDateMixin:
    @staticmethod
    def format_date(date_str: str):
        if not date_str:
            return None
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        if date_obj.tzinfo is None:
            eastern = pytz.timezone('US/Eastern')
            date_obj = eastern.localize(date_obj)
        return date_obj
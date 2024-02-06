from commuter_rail_departure.settings.settings import *
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MOCK_DATA = os.path.join(BASE_DIR, "mock_data/")


DATABASES = {
    'default': {
        "NAME": "commuter_rail_departure_unittest",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "commuter_rail_departure",
        "HOST": "localhost",
        'PASSWORD': "Testing321"
    }
}
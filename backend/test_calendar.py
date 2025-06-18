import sys
import os

# Afegeix el path absolut del projecte
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.google_calendar import create_event

create_event(
    client_name="Pol",
    service="Tallat",
    iso_datetime="2025-06-19T17:00:00",
    duration_minutes=30
)

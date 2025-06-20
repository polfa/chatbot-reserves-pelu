# backend/calendar.py
import os
import datetime
import pickle
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import timedelta
from datetime import datetime



CALENDAR_ID = 'primary'


load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_PATH = 'token.pickle'
CREDENTIALS_FILE = 'credentials.json'
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

def authenticate_google():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_event(client_name, service, iso_datetime, duration_minutes):
    creds = authenticate_google()
    service_api = build("calendar", "v3", credentials=creds)

    start = iso_datetime.isoformat()
    end_dt = iso_datetime + timedelta(minutes=duration_minutes)
    end = end_dt.isoformat()

    event = {
        "summary": f"{service} - {client_name}",
        "description": f"Reserva per {client_name}, servei: {service}",
        "start": {
            "dateTime": start,
            "timeZone": "Europe/Madrid",  # ajusta si cal
        },
        "end": {
            "dateTime": end,
            "timeZone": "Europe/Madrid",
        },
    }

    event_result = service_api.events().insert(calendarId="primary", body=event).execute()
    return event_result

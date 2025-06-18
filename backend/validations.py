import re
from datetime import datetime

def validate_name(name: str) -> str:
    # Nom: només lletres (maj/min), espais i accents, mínim 2 caràcters
    if not name or len(name.strip()) < 2:
        return "ERROR"
    pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$"
    if re.match(pattern, name.strip()):
        return name.strip()
    return "ERROR"

def validate_iso_datetime(date_str: str) -> str:
    # Esperem format "YYYY-MM-DDTHH:MM"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        if dt < datetime.now():
           return "ERROR"
        return date_str
    except ValueError:
        return "ERROR"
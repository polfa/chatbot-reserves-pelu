import re

def extract_empleat_from_message(message: str, empleats: list[str]) -> str:
    message_lower = message.lower()

    for empleat in empleats:
        empleat_lower = empleat.lower()

        # Comprova si el nom apareix dins del missatge en qualsevol lloc
        if empleat_lower in message_lower:
            return empleat  # Retorna amb l'ortografia original
    return "ERROR"

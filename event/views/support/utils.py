from datetime import datetime


def convert_string_to_time(_string, _format='%d/%m/%Y'):
    try:
        return datetime.strptime(_string, _format)
    except (ValueError, IndexError, AttributeError):
        return None

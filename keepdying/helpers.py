from datetime import datetime
def str_to_bool(value):
    if value is None:
        return False
    return value.lower() in ('yes', 'true', '1', 'on')

def str_to_int(value):
    try:
        return int(value)
    except ValueError:
        return None

def str_to_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return None
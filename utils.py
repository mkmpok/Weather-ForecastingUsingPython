# utils.py
from datetime import datetime

def validate_dates(start_date, end_date):
    """
    Ensure start and end are YYYY-MM-DD and start <= end.
    Returns (True, parsed_start, parsed_end) or (False, message)
    """
    try:
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
        ed = datetime.strptime(end_date, "%Y-%m-%d").date()
    except Exception:
        return False, "Dates must be in YYYY-MM-DD format"
    if sd > ed:
        return False, "Start date cannot be after end date"
    return True, (sd, ed)
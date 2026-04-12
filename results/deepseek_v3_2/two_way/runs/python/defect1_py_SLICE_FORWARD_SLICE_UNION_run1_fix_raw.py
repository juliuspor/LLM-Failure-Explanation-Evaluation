@classmethod
def for_offset_hours_minutes(cls, hours, minutes):
    if not (-23 <= hours <= 23):
        raise ValueError("Hours must be between -23 and 23")
    if not (0 <= minutes <= 59):
        raise ValueError("Minutes must be between 0 and 59")
    total_minutes = hours * 60 + minutes
    if not (-23*60+59 <= total_minutes <= 23*60+59):
        raise ValueError("Total offset out of range")
    offset_millis = total_minutes * 60 * 1000
    return cls.for_offset_millis(offset_millis)
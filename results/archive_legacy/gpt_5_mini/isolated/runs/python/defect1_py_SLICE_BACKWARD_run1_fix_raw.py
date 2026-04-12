@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    try:
        hours_offset_int = int(hours_offset)
    except (TypeError, ValueError):
        raise ValueError(f"Hours out of range: {hours_offset}")
    try:
        minutes_offset_int = int(minutes_offset)
    except (TypeError, ValueError):
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset_int < -23 or hours_offset_int > 23:
        raise ValueError(f"Hours out of range: {hours_offset_int}")
    if minutes_offset_int < 0 or minutes_offset_int > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset_int}")
    offset = 0
    try:
        hours_in_minutes = hours_offset_int * 60
        if hours_in_minutes < 0:
            total_minutes = hours_in_minutes - minutes_offset_int
        else:
            total_minutes = hours_in_minutes + minutes_offset_int
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
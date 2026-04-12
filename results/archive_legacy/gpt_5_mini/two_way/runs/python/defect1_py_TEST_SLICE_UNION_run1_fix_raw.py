@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError("Positive hours with negative minutes is not allowed")
    if hours_offset < 0 and minutes_offset > 0:
        raise ValueError("Negative hours with positive minutes is not allowed")
    try:
        total_minutes = hours_offset * 60
        if hours_offset >= 0:
            total_minutes = total_minutes + minutes_offset
        else:
            total_minutes = total_minutes - abs(minutes_offset)
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    offset = 0
    try:
        hours_in_minutes = hours_offset * 60
        if hours_in_minutes < 0:
            minutes_total = hours_in_minutes - minutes_offset
        else:
            minutes_total = hours_in_minutes + minutes_offset
        offset = FieldUtils.safe_multiply(minutes_total, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
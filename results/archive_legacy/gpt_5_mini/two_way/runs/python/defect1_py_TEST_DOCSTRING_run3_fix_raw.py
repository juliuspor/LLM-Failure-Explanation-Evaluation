@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    sign = 1
    if hours_offset < 0:
        sign = -1
    elif hours_offset == 0 and minutes_offset < 0:
        sign = -1
    total_minutes = 0
    if hours_offset != 0:
        total_minutes = abs(hours_offset) * 60 + abs(minutes_offset)
    else:
        total_minutes = abs(minutes_offset)
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    offset = sign * offset
    return cls.for_offset_millis(offset)
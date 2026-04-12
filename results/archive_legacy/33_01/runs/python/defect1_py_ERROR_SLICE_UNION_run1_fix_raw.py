@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError("Minutes must be positive when hours is positive")
    if hours_offset < 0 and minutes_offset > 0:
        minutes_sign = 1
    # determine sign
    if hours_offset < 0:
        sign = -1
    elif hours_offset > 0:
        sign = 1
    else:
        sign = -1 if minutes_offset < 0 else 1
    minutes_abs = abs(minutes_offset)
    try:
        total_minutes = abs(hours_offset) * 60 + minutes_abs
        total_minutes = sign * total_minutes
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
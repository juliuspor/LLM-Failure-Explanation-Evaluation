@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    # Disallow mixed signs like (2, -15) or (-2, 15)
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset < 0 and minutes_offset > 0:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    # Determine overall sign: from hours if non-zero, else from minutes
    if hours_offset > 0:
        sign = 1
    elif hours_offset < 0:
        sign = -1
    else:
        sign = 1 if minutes_offset > 0 else -1
    hours_abs = abs(hours_offset)
    minutes_abs = abs(minutes_offset)
    try:
        total_minutes = FieldUtils.safe_multiply(hours_abs, 60) + minutes_abs
        total_millis = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        if sign < 0:
            total_millis = -total_millis
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(total_millis)
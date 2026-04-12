@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Determine sign for the combined offset. If hours_offset is non-zero, its sign dominates.
    sign = 1
    if hours_offset < 0:
        sign = -1
    elif hours_offset > 0:
        sign = 1
    else:
        # hours_offset == 0 -> sign comes from minutes_offset
        if minutes_offset < 0:
            sign = -1
        else:
            sign = 1
    abs_minutes = abs(minutes_offset)
    if abs_minutes < 0 or abs_minutes > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        total_minutes = hours_offset * 60 + sign * abs_minutes
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
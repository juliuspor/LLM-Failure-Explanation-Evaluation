@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    abs_minutes = abs(minutes_offset)
    if abs_minutes < 0 or abs_minutes > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Determine sign from hours_offset; if hours_offset is zero, use sign of minutes_offset
        if hours_offset < 0:
            total_minutes = hours_offset * 60 - abs_minutes
        elif hours_offset > 0:
            total_minutes = hours_offset * 60 + abs_minutes
        else:
            # hours_offset == 0
            total_minutes = -abs_minutes if minutes_offset < 0 else abs_minutes
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if abs(minutes_offset) < 0 or abs(minutes_offset) > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Determine sign to apply to minutes. If hours_offset is non-zero, its sign applies.
        # If hours_offset is zero, the sign of minutes_offset determines overall sign.
        if hours_offset > 0:
            total_minutes = hours_offset * 60 + abs(minutes_offset)
        elif hours_offset < 0:
            total_minutes = hours_offset * 60 - abs(minutes_offset)
        else:
            # hours_offset == 0
            if minutes_offset < 0:
                total_minutes = -abs(minutes_offset)
            else:
                total_minutes = abs(minutes_offset)
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
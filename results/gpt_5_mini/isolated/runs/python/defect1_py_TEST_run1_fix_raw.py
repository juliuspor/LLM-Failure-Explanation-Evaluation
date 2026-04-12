@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Determine sign for the combined offset. If hours is negative, the
        # total minutes should be negative. If hours is zero, the sign is
        # determined by minutes_offset (positive only allowed here so zero
        # hours means positive minutes).
        total_minutes = hours_offset * 60
        if hours_offset < 0:
            total_minutes -= minutes_offset
        else:
            total_minutes += minutes_offset
        millis = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(millis)
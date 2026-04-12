@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    # Disallow mixed sign inputs like (2, -15) or (-2, 15)
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError("Positive hours with negative minutes is not supported")
    if hours_offset < 0 and minutes_offset > 0:
        # minutes should be treated as negative when hours is negative
        pass
    try:
        # Compute total minutes without mutating inputs
        if hours_offset < 0:
            total_minutes = hours_offset * 60 - abs(minutes_offset)
        else:
            total_minutes = hours_offset * 60 + abs(minutes_offset)
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
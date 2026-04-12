@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    # Combine hours and minutes into total minutes, handling signs correctly.
    # If either component is negative, treat the total sign as negative.
    total_minutes = hours_offset * 60
    if minutes_offset != 0:
        # If hours and minutes have opposite signs, this is ambiguous;
        # determine sign from hours if non-zero, otherwise from minutes.
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError("Hours and minutes must have the same sign")
        if hours_offset < 0 and minutes_offset > 0:
            raise ValueError("Hours and minutes must have the same sign")
        total_minutes += minutes_offset if hours_offset >= 0 else -abs(minutes_offset)
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
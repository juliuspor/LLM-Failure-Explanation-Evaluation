@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Allow minutes to be negative to represent negative offsets, but absolute value must be within 0..59
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    # Disallow mixed sign combinations like (2, -15) or (-2, 15)
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError(f"Illegal combination of hours and minutes: {hours_offset}, {minutes_offset}")
    if hours_offset < 0 and minutes_offset > 0:
        raise ValueError(f"Illegal combination of hours and minutes: {hours_offset}, {minutes_offset}")
    try:
        # Compute total minutes, taking into account sign of hours and minutes
        if hours_offset < 0 or minutes_offset < 0:
            # If either is negative, total minutes should be negative
            total_minutes = -(abs(hours_offset) * 60 + abs(minutes_offset))
        else:
            total_minutes = hours_offset * 60 + minutes_offset
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
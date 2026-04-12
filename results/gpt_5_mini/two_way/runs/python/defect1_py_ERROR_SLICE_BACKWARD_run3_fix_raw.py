@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Allow minutes_offset to be negative by normalizing it relative to hours
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Combine hours and minutes into total minutes, preserving sign semantics.
        # If hours_offset is negative, the overall sign is negative; otherwise positive.
        sign = -1 if hours_offset < 0 else 1
        # If hours is zero, sign should come from minutes_offset if negative
        if hours_offset == 0 and minutes_offset < 0:
            sign = -1
        total_minutes = abs(hours_offset) * 60 + abs(minutes_offset)
        total_minutes *= sign
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Allow minutes to be negative when representing negative offsets
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    # If hours and minutes have opposite signs, that's ambiguous (except zero hour)
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError("Hours and minutes must have the same sign")
    if hours_offset < 0 and minutes_offset > 0:
        raise ValueError("Hours and minutes must have the same sign")
    try:
        total_minutes = hours_offset * 60 + (minutes_offset if hours_offset >= 0 else -abs(minutes_offset))
        # If hours_offset is negative, ensure minutes contribute negatively.
        # The above handles cases where minutes_offset may already be negative.
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
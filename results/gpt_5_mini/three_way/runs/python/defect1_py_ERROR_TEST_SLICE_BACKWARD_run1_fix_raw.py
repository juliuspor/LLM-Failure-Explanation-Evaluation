@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Compute total minutes, respecting sign of hours and minutes
        total_minutes = hours_offset * 60
        # If hours is negative and minutes positive, or hours positive and minutes negative,
        # the signs should combine to produce the correct total offset.
        total_minutes += minutes_offset if hours_offset >= 0 else -abs(minutes_offset)
        # However, the above line would double-negate when minutes_offset already negative and hours negative,
        # so better to compute using absolute logic:
    except Exception:
        raise ValueError("Offset is too large")
    # Recompute safely to ensure correct handling for mixed signs
    # Use explicit logic:
    if hours_offset >= 0:
        total_minutes = hours_offset * 60 + minutes_offset
    else:
        total_minutes = hours_offset * 60 - minutes_offset if minutes_offset > 0 else hours_offset * 60 + minutes_offset
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
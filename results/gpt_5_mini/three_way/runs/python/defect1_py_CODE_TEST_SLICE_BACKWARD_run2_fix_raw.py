@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Compute total minutes preserving the intended sign.
        total_minutes = hours_offset * 60 + minutes_offset
        # Handle cases where hours_offset is negative but minutes_offset positive
        # e.g., hours=-2, minutes=15 should produce -135 minutes.
        if hours_offset < 0 and minutes_offset > 0:
            total_minutes = hours_offset * 60 - minutes_offset
        # Conversely, hours positive and minutes negative should subtract minutes
        if hours_offset > 0 and minutes_offset < 0:
            total_minutes = hours_offset * 60 + minutes_offset
        # When hours_offset is zero, minutes_offset sign stands as provided.
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
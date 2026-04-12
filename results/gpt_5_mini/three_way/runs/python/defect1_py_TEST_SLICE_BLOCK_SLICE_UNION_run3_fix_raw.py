@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Allow minutes to be negative so callers can pass -15 for negative offsets.
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")

    # Validate sign compatibility: minutes must have same sign as hours unless hours is zero.
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError("Mixed sign: hours positive but minutes negative")
    if hours_offset < 0 and minutes_offset > 0:
        raise ValueError("Mixed sign: hours negative but minutes positive")

    try:
        # Combine hours and minutes into total minutes
        total_minutes = hours_offset * 60 + minutes_offset
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Normalize sign: allow minutes_offset to be negative and combine with hours
    # Compute total minutes by applying the sign of hours if minutes has no sign
    # If hours_offset is negative, total minutes should be negative.
    # If hours_offset is zero, minutes_offset may carry its own sign.
    total_minutes = hours_offset * 60 + minutes_offset
    # Validate that total_minutes is within allowed range (-23:59..+23:59)
    if total_minutes < -23 * 60 - 59 or total_minutes > 23 * 60 + 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
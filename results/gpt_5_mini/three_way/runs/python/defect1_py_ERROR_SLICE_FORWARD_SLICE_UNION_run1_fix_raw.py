@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Determine sign from hours_offset (if hours is zero, sign comes from minutes)
        sign = -1 if hours_offset < 0 else 1
        if hours_offset == 0 and minutes_offset != 0:
            # If hours is zero, sign should reflect minutes_offset's sign possibility
            # but minutes_offset is expected positive per validation above, so keep positive
            sign = 1
        total_minutes = abs(hours_offset) * 60 + minutes_offset
        total_minutes *= sign
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
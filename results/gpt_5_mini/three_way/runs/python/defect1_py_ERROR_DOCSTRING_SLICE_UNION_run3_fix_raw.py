@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Normalize by allowing minutes_offset to carry sign and combine into total minutes
    total_minutes = hours_offset * 60 + minutes_offset
    # Validate total range: from -23:59 to +23:59 in minutes
    max_minutes = 23 * 60 + 59
    if total_minutes < -max_minutes or total_minutes > max_minutes:
        raise ValueError(f"Minutes out of range: {minutes_offset} (combined total minutes {total_minutes})")
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
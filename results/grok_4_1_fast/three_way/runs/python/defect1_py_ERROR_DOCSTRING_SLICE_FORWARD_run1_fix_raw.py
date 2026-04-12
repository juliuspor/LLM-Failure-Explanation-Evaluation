@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    """
    Create a fixed-offset time zone for the given UTC offset.

    The offset is provided as an hours component plus a minutes component and
    is converted to a millisecond offset for the resulting `DateTimeZone`.

    Args:
        hours_offset: Offset in hours relative to UTC (-23 to +23).
        minutes_offset: Offset minutes component (within a single hour).
        
    Returns:
        A `DateTimeZone` instance representing the requested fixed offset.
        
    Raises:
        ValueError: If the provided values are out of range or the resulting offset
            is not supported.
    """
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    # Compute total minutes and normalize to hours + minutes (0-59)
    total_minutes = hours_offset * 60 + minutes_offset
    # Normalize: adjust hours and ensure minutes is 0-59
    normalized_hours = total_minutes // 60
    normalized_minutes = total_minutes % 60
    if normalized_minutes < 0:
        normalized_minutes += 60
        normalized_hours -= 1
    offset = 0
    try:
        offset = FieldUtils.safe_multiply(normalized_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        offset = FieldUtils.safe_multiply(normalized_hours, DateTimeConstants.MILLIS_PER_HOUR) + offset
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)

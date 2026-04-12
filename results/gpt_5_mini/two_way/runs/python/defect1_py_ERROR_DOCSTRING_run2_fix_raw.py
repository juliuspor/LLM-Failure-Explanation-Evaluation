@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC

    # Combine hours and minutes into total minutes, allowing minutes_offset to be signed
    # Normalize: if hours_offset is negative and minutes_offset is positive, the total should be negative
    total_minutes = hours_offset * 60 + minutes_offset

    # Validate combined range: from -23:59 to +23:59 in minutes
    min_minutes = -23 * 60 - 59
    max_minutes = 23 * 60 + 59
    if total_minutes < min_minutes or total_minutes > max_minutes:
        raise ValueError(f"Combined hours and minutes out of range: hours={hours_offset}, minutes={minutes_offset}")

    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")

    return cls.for_offset_millis(offset)
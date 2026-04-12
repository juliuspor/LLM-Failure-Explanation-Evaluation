@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError("Positive hours cannot be combined with negative minutes")
    total_seconds = hours_offset * 3600 + minutes_offset * 60
    max_seconds = 23 * 3600 + 59 * 60 + 59
    if abs(total_seconds) > max_seconds:
        raise ValueError("Resulting offset exceeds +/- 23:59:59.000")
    try:
        hours_in_minutes = hours_offset * 60
        if hours_in_minutes < 0:
            minutes_total = hours_in_minutes - minutes_offset
        else:
            minutes_total = hours_in_minutes + minutes_offset
        offset = FieldUtils.safe_multiply(minutes_total, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
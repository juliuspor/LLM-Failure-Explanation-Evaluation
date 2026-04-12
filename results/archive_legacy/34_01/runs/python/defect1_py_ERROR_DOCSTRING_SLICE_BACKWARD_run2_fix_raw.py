@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    total_minutes = hours_offset * 60 + minutes_offset
    max_minutes = 23 * 60 + 59
    if total_minutes < -max_minutes or total_minutes > max_minutes:
        raise ValueError(f"Hours and minutes out of range: {hours_offset}, {minutes_offset}")
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
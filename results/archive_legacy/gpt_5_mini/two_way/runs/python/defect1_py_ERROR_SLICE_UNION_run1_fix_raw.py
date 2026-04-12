@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    minutes_parsed = minutes_offset
    if abs(minutes_parsed) > 59:
        raise ValueError(f"Minutes out of range: {minutes_parsed}")
    try:
        hours_in_minutes = hours_offset * 60
        if hours_in_minutes < 0:
            total_minutes = hours_in_minutes - abs(minutes_parsed)
        else:
            total_minutes = hours_in_minutes + abs(minutes_parsed)
        if hours_in_minutes == 0 and minutes_parsed < 0:
            total_minutes = -abs(minutes_parsed)
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
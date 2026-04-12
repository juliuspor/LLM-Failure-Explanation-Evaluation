@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    minutes_abs = abs(minutes_offset)
    if minutes_abs > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError("Minutes must be positive when hours are positive")
    if hours_offset < 0 and minutes_offset > 0:
        raise ValueError("Minutes must be negative when hours are negative")
    try:
        total_minutes = hours_offset * 60
        if hours_offset < 0:
            total_minutes -= minutes_abs
        else:
            total_minutes += (minutes_abs if hours_offset != 0 else ( -minutes_abs if minutes_offset < 0 else minutes_abs))
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
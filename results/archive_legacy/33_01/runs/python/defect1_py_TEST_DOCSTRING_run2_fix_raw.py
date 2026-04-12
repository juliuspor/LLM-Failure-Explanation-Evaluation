@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset > 0:
        sign = 1
    elif hours_offset < 0:
        sign = -1
    else:
        sign = 1 if minutes_offset >= 0 else -1
    total_minutes = sign * (abs(hours_offset) * 60 + abs(minutes_offset))
    max_minutes = 23 * 60 + 59
    if total_minutes < -max_minutes or total_minutes > max_minutes:
        raise ValueError("Resulting offset is too large")
    try:
        millis = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(millis)
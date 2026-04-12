@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError("Minutes out of range: minutes must not be negative when hours is positive")
    if hours_offset != 0:
        minutes_signed = (1 if hours_offset > 0 else -1) * abs(minutes_offset)
    else:
        minutes_signed = minutes_offset
    total_minutes = hours_offset * 60 + minutes_signed
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
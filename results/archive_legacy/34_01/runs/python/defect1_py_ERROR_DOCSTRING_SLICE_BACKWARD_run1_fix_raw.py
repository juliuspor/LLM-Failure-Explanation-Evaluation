@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError(f"Minutes negative when hours positive: {hours_offset}, {minutes_offset}")
    try:
        hours_in_minutes = hours_offset * 60
        if hours_in_minutes < 0:
            total_minutes = hours_in_minutes - minutes_offset
        else:
            total_minutes = hours_in_minutes + minutes_offset
        total_seconds = total_minutes * 60
        if abs(total_seconds) > (23 * 3600 + 59 * 60 + 59):
            raise ValueError("Offset is too large")
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
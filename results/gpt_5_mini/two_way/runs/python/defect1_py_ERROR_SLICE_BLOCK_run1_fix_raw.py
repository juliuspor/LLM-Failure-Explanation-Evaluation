@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Accept minutes_offset possibly signed; only its absolute value must be within 0..59
    abs_minutes = minutes_offset if minutes_offset >= 0 else -minutes_offset
    if abs_minutes < 0 or abs_minutes > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Determine combined minutes with sign from hours_offset. If hours_offset is zero, use sign of minutes_offset.
        sign = -1 if hours_offset < 0 else ( -1 if hours_offset == 0 and minutes_offset < 0 else 1)
        hours_in_minutes = abs(hours_offset) * 60
        total_minutes = hours_in_minutes + abs_minutes
        total_minutes = total_minutes * sign
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
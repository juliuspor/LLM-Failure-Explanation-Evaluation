@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    total_minutes = hours_offset * 60 + minutes_offset
    if total_minutes < - (23 * 60 + 59) or total_minutes > (23 * 60 + 59):
        raise ValueError("Offset is too large")
    sign = 1 if total_minutes >= 0 else -1
    abs_total = abs(total_minutes)
    norm_hours = (abs_total // 60) * sign
    norm_minutes = abs_total % 60
    try:
        minutes_total = norm_hours * 60 + (norm_minutes if norm_hours >= 0 else -norm_minutes)
        offset = FieldUtils.safe_multiply(minutes_total, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
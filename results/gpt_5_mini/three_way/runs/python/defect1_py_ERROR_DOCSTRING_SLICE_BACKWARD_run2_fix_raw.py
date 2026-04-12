@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Combine hours and minutes into total minutes, allowing minutes_offset to be negative
    # minutes_offset is interpreted as the minute component to add to hours_offset.
    sign = -1 if (hours_offset < 0) else 1
    total_minutes = hours_offset * 60 + sign * minutes_offset if hours_offset != 0 else minutes_offset if minutes_offset >= 0 else -minutes_offset * -1
    # The above line attempts to respect sign of hours; simpler approach:
    # Compute total as hours*60 + minutes with minutes taking its own sign
    total_minutes = hours_offset * 60 + minutes_offset
    # Validate total_minutes within -23:59 .. +23:59 in minutes
    if total_minutes < (-23 * 60 - 59) or total_minutes > (23 * 60 + 59):
        raise ValueError(f"Offset minutes out of range: {total_minutes}")
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
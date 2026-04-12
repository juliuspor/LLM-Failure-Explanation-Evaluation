@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # allow negative minutes to represent negative offsets like (0, -15)
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    offset = 0
    try:
        hours_in_minutes = hours_offset * 60
        # combine hours and minutes taking into account signs
        if hours_in_minutes < 0:
            total_minutes = hours_in_minutes - abs(minutes_offset)
        else:
            total_minutes = hours_in_minutes + minutes_offset
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
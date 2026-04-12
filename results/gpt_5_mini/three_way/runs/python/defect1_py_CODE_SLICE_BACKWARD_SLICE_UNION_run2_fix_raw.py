@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        total_minutes = hours_offset * 60
        # Apply sign of hours to the minutes component. If hours is negative,
        # the minutes should subtract from the total (e.g. -1 hours and 30 minutes -> -90 minutes).
        if hours_offset < 0:
            total_minutes -= minutes_offset
        else:
            total_minutes += minutes_offset
        millis = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(millis)
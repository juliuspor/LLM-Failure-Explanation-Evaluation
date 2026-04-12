@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # minutes_offset should represent the magnitude of minutes within the hour
    # Allow callers to pass a negative minutes_offset only in conjunction with
    # a negative hours_offset; treat minutes as absolute magnitude here.
    minutes_abs = minutes_offset
    if minutes_abs < 0:
        minutes_abs = -minutes_abs
    if minutes_abs < 0 or minutes_abs > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # combine hours and minutes into total minutes, preserving sign of hours
        if hours_offset < 0:
            total_minutes = hours_offset * 60 - minutes_abs
        else:
            total_minutes = hours_offset * 60 + minutes_abs
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
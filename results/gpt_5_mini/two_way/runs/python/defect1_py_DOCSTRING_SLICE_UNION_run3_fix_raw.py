@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Apply sign of hours to minutes component. If hours is negative,
        # the minutes should also be treated as negative.
        if hours_offset < 0:
            total_minutes = hours_offset * 60 - minutes_offset
        else:
            total_minutes = hours_offset * 60 + minutes_offset
        # Validate combined range: maximum magnitude allowed is 23*60 + 59
        max_minutes = 23 * 60 + 59
        if total_minutes < -max_minutes or total_minutes > max_minutes:
            raise ValueError("Offset is too large")
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
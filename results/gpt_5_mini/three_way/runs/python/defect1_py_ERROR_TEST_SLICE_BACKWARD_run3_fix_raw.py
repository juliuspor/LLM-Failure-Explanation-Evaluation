@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # minutes_offset may be negative to indicate negative offset when hours negative
    if abs(minutes_offset) > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Determine the sign for minutes: if hours_offset is non-zero, minutes follow its sign;
        # otherwise minutes_offset's sign determines overall sign.
        if hours_offset != 0:
            sign = -1 if hours_offset < 0 else 1
            total_minutes = hours_offset * 60 + sign * abs(minutes_offset)
        else:
            # hours is zero, minutes_offset may carry sign
            total_minutes = minutes_offset
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
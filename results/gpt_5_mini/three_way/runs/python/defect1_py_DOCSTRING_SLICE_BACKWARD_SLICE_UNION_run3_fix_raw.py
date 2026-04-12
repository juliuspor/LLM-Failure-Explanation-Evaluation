@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    # Compute total minutes taking into account the sign of hours_offset
    try:
        hours_in_minutes = hours_offset * 60
        if hours_offset < 0:
            total_minutes = hours_in_minutes - minutes_offset
        else:
            total_minutes = hours_in_minutes + minutes_offset
        # Validate total_minutes is within allowed range (-23*60 -59 .. +23*60 +59)
        if total_minutes < - (23 * 60 + 59) or total_minutes > (23 * 60 + 59):
            raise ValueError(f"Offset is too large: {hours_offset} hours and {minutes_offset} minutes")
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
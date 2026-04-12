@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Normalize minutes to total minutes taking sign into account
        total_minutes = hours_offset * 60
        if total_minutes < 0:
            # hours negative, minutes should subtract (more negative if minutes positive)
            total_minutes -= abs(minutes_offset)
        else:
            # hours positive or zero, minutes should add/subtract according to sign of minutes_offset
            total_minutes += minutes_offset
        # If hours_offset is zero, minutes_offset sign determines direction (handled above)
        # Validate total within allowable range: -23:59..+23:59 in minutes
        if total_minutes < -(23 * 60 + 59) or total_minutes > (23 * 60 + 59):
            raise ValueError("Offset is too large")
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
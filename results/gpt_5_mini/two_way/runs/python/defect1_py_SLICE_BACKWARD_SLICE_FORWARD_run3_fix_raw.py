@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Combine hours and minutes into total minutes, allowing minutes_offset to be negative
    try:
        total_minutes = hours_offset * 60
        # If hours is negative, minutes should subtract; otherwise add
        if total_minutes < 0:
            total_minutes -= abs(minutes_offset)
        else:
            total_minutes += abs(minutes_offset)
        # Preserve sign if hours was zero: minutes_offset sign determines
        if hours_offset == 0:
            if minutes_offset < 0:
                total_minutes = -abs(minutes_offset)
            else:
                total_minutes = abs(minutes_offset)
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
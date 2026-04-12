@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        # Determine the sign to apply to minutes. If hours_offset is non-zero,
        # its sign determines the overall sign. If hours_offset is zero, use
        # the sign of minutes_offset (allowing offsets like -00:30 via negative minutes).
        if hours_offset > 0:
            total_minutes = hours_offset * 60 + minutes_offset
        elif hours_offset < 0:
            total_minutes = hours_offset * 60 - minutes_offset
        else:
            # hours_offset == 0: minutes_offset's sign determines offset
            total_minutes = minutes_offset
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        hours_in_minutes = hours_offset * 60
        total_minutes = hours_in_minutes + (minutes_offset if hours_offset >= 0 else -minutes_offset if minutes_offset != 0 and minutes_offset > 0 and hours_offset < 0 else minutes_offset)
        # The above line ensures that a positive minutes_offset with a negative hours_offset
        # results in a subtraction (e.g., -2 hours and 15 minutes -> -135 minutes).
        # However, if minutes_offset was provided negative (which we've disallowed above),
        # this branch will not be reached. Keep simple: total_minutes = hours_in_minutes + (hours_offset < 0 and -minutes_offset or minutes_offset)
        # Simpler replacement below to avoid confusion:
    except ArithmeticError:
        raise ValueError("Offset is too large")
    # Simpler, correct computation of total_minutes
    hours_in_minutes = hours_offset * 60
    # If hours_offset is negative, the minutes component should also subtract from the total offset
    if hours_offset < 0:
        total_minutes = hours_in_minutes - minutes_offset
    else:
        total_minutes = hours_in_minutes + minutes_offset
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
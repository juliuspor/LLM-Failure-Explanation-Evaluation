@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < 0 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    # Determine the sign: if hours is negative then overall sign is negative.
    # If hours is zero, then sign is determined by minutes (allow negative minutes via caller convention)
    sign = -1 if hours_offset < 0 else 1
    # If hours_offset is zero but minutes_offset should be negative, caller must pass hours_offset=0 and negative minutes -
    # However API expects minutes_offset 0..59, so handle case where hours_offset==0 and caller intended negative via separate sign
    # We'll treat hours_offset==0 as sign based on provided minutes_offset only if caller passed minutes_offset with sign encoded
    # Since minutes_offset is validated >=0, we use sign from hours_offset only.
    total_minutes = hours_offset * 60 + sign * minutes_offset
    try:
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
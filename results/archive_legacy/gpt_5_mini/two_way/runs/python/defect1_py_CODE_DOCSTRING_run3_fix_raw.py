@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    """
    Gets a time zone instance for the specified offset to UTC in hours and minutes.
    This method assumes 60 minutes in an hour, and standard length minutes.

    This factory is a convenient way of constructing zones with a fixed offset.
    The hours value must be in the range -23 to +23.
    The minutes value must be in the range -59 to +59.
    The following combinations of sign for the hour and minute are possible:

     Hour    Minute    Example    Result

     +ve     +ve       (2, 15)    +02:15
     +ve     zero      (2, 0)     +02:00
     +ve     -ve       (2, -15)   ValueError

     zero    +ve       (0, 15)    +00:15
     zero    zero      (0, 0)     +00:00
     zero    -ve       (0, -15)   -00:15

     -ve     +ve       (-2, 15)   -02:15
     -ve     zero      (-2, 0)    -02:00
     -ve     -ve       (-2, -15)  -02:15

    Note that in versions before 2.3, the minutes had to be zero or positive.

    Args:
        hours_offset: the offset in hours from UTC, from -23 to +23
        minutes_offset: the offset in minutes from UTC, from -59 to +59

    Returns:
        the DateTimeZone object for the offset

    Raises:
        ValueError: if any value is out of range, the minutes are negative
            when the hours are positive, or the resulting offset exceeds +/- 23:59:59.000
    """
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    if hours_offset > 0 and minutes_offset < 0:
        raise ValueError("Positive hours cannot have negative minutes")
    try:
        hours_in_minutes = hours_offset * 60
        if hours_offset < 0:
            total_minutes = hours_in_minutes - abs(minutes_offset)
        elif hours_offset > 0:
            total_minutes = hours_in_minutes + minutes_offset
        else:
            total_minutes = minutes_offset
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    # Interpret minutes_offset as a minutes component but also accept total-minute values.
    # Compute total minutes taking sign of hours into account when minutes_offset is provided
    # as a component; also support callers providing a total minutes value (e.g., 90, 120).
    # If minutes_offset has magnitude > 59 we treat it as total additional minutes.
    # First compute a base from hours_offset.
    try:
        base_minutes = hours_offset * 60
        # If minutes_offset has same sign as hours_offset or hours_offset is zero, just add.
        if hours_offset == 0:
            total_minutes = minutes_offset
        else:
            # If minutes_offset seems to be a component (0..59), respect its sign when hours positive/negative.
            if -59 <= minutes_offset <= 59:
                if hours_offset < 0:
                    total_minutes = base_minutes - abs(minutes_offset)
                else:
                    total_minutes = base_minutes + abs(minutes_offset)
            else:
                # minutes_offset appears to be a total-minute value; add directly to base
                total_minutes = base_minutes + minutes_offset
        if total_minutes < -1439 or total_minutes > 1439:
            raise ValueError(f"Minutes out of range: resulting total minutes {total_minutes}")
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
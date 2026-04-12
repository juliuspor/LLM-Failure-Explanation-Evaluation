@classmethod
def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
    if hours_offset == 0 and minutes_offset == 0:
        return cls.UTC
    if hours_offset < -23 or hours_offset > 23:
        raise ValueError(f"Hours out of range: {hours_offset}")
    if minutes_offset < -59 or minutes_offset > 59:
        raise ValueError(f"Minutes out of range: {minutes_offset}")
    try:
        total_minutes = hours_offset * 60 + (minutes_offset if hours_offset >= 0 else -minutes_offset if minutes_offset < 0 else minutes_offset)
        # The above preserves the sign of hours and minutes appropriately.
        # More simply, combine hours and minutes with the sign of hours when hours non-zero,
        # otherwise minutes sign stands as provided.
        if hours_offset != 0:
            # If hours is negative, total minutes should be negative when minutes positive
            # e.g., hours=-2, minutes=15 -> total_minutes = - (abs(hours)*60) - 15
            if hours_offset < 0:
                total_minutes = hours_offset * 60 - abs(minutes_offset)
            else:
                total_minutes = hours_offset * 60 + abs(minutes_offset)
        else:
            total_minutes = minutes_offset
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
    except ArithmeticError:
        raise ValueError("Offset is too large")
    return cls.for_offset_millis(offset)
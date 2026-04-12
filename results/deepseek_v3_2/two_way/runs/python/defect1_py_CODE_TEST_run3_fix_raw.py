    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        offset = 0
        try:
            total_minutes = hours_offset * 60
            if total_minutes < 0:
                # Both hours_offset and minutes_offset have signs; we need to combine them.
                # If minutes_offset is positive, we subtract it (since hours_offset is negative).
                # If minutes_offset is negative, we add it (since both are negative).
                total_minutes += minutes_offset
            else:
                total_minutes += minutes_offset
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
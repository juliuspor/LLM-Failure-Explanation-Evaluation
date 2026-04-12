@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Disallow mixed signs (e.g., hours positive and minutes negative) unless hours == 0
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        if hours_offset < 0 and minutes_offset > 0:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Determine overall sign
        sign = -1 if (hours_offset < 0 or (hours_offset == 0 and minutes_offset < 0)) else 1
        abs_hours = abs(hours_offset)
        abs_minutes = abs(minutes_offset)
        try:
            total_minutes = FieldUtils.safe_multiply(abs_hours, 60) + abs_minutes
            total_millis = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
            offset = sign * total_millis
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Reject mixed sign where hours positive and minutes negative or vice versa
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError("Positive hours with negative minutes is invalid")
        if hours_offset < 0 and minutes_offset > 0:
            # Treat positive minutes with negative hours as extending the negative magnitude
            minutes_abs = minutes_offset
        else:
            minutes_abs = abs(minutes_offset)
        # Determine sign: if hours non-zero use its sign, otherwise use minutes sign
        if hours_offset < 0:
            sign = -1
        elif hours_offset > 0:
            sign = 1
        else:
            sign = -1 if minutes_offset < 0 else 1
        total_minutes = abs(hours_offset) * 60 + minutes_abs
        try:
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        if sign < 0:
            offset = -offset
        return cls.for_offset_millis(offset)
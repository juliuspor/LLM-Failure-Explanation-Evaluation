@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        sign = -1 if hours_offset < 0 else 1
        minutes_abs = minutes_offset if minutes_offset >= 0 else -minutes_offset
        if minutes_abs < 0 or minutes_abs > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        try:
            hours_in_minutes = abs(hours_offset) * 60
            total_minutes = hours_in_minutes + minutes_abs
            if sign < 0:
                total_minutes = -total_minutes
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        try:
            # Determine the sign: if hours_offset is non-zero use its sign,
            # otherwise use the sign of minutes_offset (shouldn't be zero here).
            if hours_offset > 0:
                sign = 1
            elif hours_offset < 0:
                sign = -1
            else:
                # hours_offset == 0, minutes_offset can be positive only per validation
                sign = 1
            total_minutes = abs(hours_offset) * 60 + minutes_offset
            total_minutes *= sign
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
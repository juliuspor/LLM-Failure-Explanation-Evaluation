@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        try:
            # Determine sign: if hours_offset is negative then whole offset is negative.
            sign = -1 if hours_offset < 0 else 1
            # If hours is zero, the sign should be taken from minutes_offset? Keep sign positive for zero hours
            # so that for_offset_hours_minutes(0, -15) is invalid due to minutes range check above.
            total_minutes = hours_offset * 60 + sign * minutes_offset
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
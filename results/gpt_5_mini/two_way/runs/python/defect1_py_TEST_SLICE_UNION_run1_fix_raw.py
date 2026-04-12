@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        try:
            # Combine hours and minutes into total minutes, preserving sign semantics
            total_minutes = hours_offset * 60
            # If hours and minutes have opposite signs, that is invalid (e.g., 1 and -30)
            if hours_offset > 0 and minutes_offset < 0:
                raise ValueError(f"Minutes out of range: {minutes_offset} for positive hours: {hours_offset}")
            if hours_offset < 0 and minutes_offset > 0:
                raise ValueError(f"Minutes out of range: {minutes_offset} for negative hours: {hours_offset}")
            total_minutes += minutes_offset
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
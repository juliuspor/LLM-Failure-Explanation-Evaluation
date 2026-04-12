@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if abs(minutes_offset) > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError("Positive hours must not have negative minutes")
        if hours_offset < 0 and minutes_offset > 0:
            minutes_total = hours_offset * 60 - minutes_offset
        else:
            minutes_total = hours_offset * 60 + minutes_offset
        try:
            offset = FieldUtils.safe_multiply(minutes_total, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
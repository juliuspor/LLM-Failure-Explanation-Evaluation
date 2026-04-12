@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        # Normalize minutes into hours, allowing minutes_offset outside 0..59
        # Compute total minutes combining hours and minutes, preserving sign of hours_offset when hours_offset != 0
        # If hours_offset is zero, sign of minutes determines direction
        total_minutes = hours_offset * 60 + minutes_offset
        # Now compute normalized hours and minutes for validation
        norm_hours = total_minutes // 60
        norm_minutes = abs(total_minutes % 60)
        if norm_hours < -23 or norm_hours > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if norm_minutes < 0 or norm_minutes > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        try:
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
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
            # Convert hours to minutes and combine with minutes_offset, preserving sign.
            # If hours_offset is negative, both components are negative.
            total_minutes = hours_offset * 60
            if total_minutes < 0:
                # Both hours and minutes are negative, so subtract positive minutes_offset?
                # Actually, minutes_offset is non-negative (0-59). For negative hours, we need to subtract minutes_offset.
                # Example: hours_offset = -2, minutes_offset = 15 => total minutes = -2*60 - 15 = -135
                total_minutes -= minutes_offset
            else:
                total_minutes += minutes_offset
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
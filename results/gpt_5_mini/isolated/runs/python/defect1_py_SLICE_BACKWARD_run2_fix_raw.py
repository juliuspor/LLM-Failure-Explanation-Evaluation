@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        # Normalize minutes so that its absolute value is within 0..59
        # Accept signed minutes (e.g. -15) and values >=60 by carrying into hours
        sign = -1 if (hours_offset < 0 or minutes_offset < 0) else 1
        # Work with absolute values to carry correctly
        abs_minutes = abs(minutes_offset)
        extra_hours = abs_minutes // 60
        rem_minutes = abs_minutes % 60
        # Adjust hours by extra_hours
        if hours_offset < 0:
            hours = hours_offset - extra_hours
        else:
            hours = hours_offset + extra_hours
        # After carrying, rem_minutes should be within 0..59
        if rem_minutes < 0 or rem_minutes > 59:
            raise ValueError(f"Minutes out of range after normalization: {minutes_offset}")
        # Validate hours now in range
        if hours < -23 or hours > 23:
            raise ValueError(f"Hours out of range after normalization: {hours}")
        # Reconstruct signed minutes component
        minutes = rem_minutes if sign >= 0 else -rem_minutes
        try:
            total_minutes = hours * 60 + minutes
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
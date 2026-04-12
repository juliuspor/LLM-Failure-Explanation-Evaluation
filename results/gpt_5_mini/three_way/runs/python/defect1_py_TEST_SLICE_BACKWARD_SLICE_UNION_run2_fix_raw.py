@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        # minutes_offset may be negative when hours_offset is negative or zero.
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Ensure minutes and hours have consistent sign (minutes can be negative if hours is negative or zero)
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError("Hours and minutes must have the same sign")
        if hours_offset < 0 and minutes_offset > 0:
            raise ValueError("Hours and minutes must have the same sign")
        try:
            total_minutes = hours_offset * 60 + (minutes_offset if hours_offset >= 0 else -abs(minutes_offset))
            # If hours_offset is negative, minutes_offset should subtract; for positive, add.
            # However above sign checks ensure consistency, so simpler compute:
            if hours_offset < 0 and minutes_offset <= 0:
                total_minutes = hours_offset * 60 - abs(minutes_offset)
            elif hours_offset >= 0 and minutes_offset >= 0:
                total_minutes = hours_offset * 60 + minutes_offset
            # Handle case hours_offset == 0 with negative minutes (e.g., 0, -15 -> -15 minutes)
            if hours_offset == 0 and minutes_offset < 0:
                total_minutes = minutes_offset
            millis = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(millis)
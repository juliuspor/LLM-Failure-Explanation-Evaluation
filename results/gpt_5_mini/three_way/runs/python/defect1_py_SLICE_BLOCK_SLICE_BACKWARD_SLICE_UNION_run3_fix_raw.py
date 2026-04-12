@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        # Normalize minutes with hours to compute total minutes offset
        try:
            hours_in_minutes = hours_offset * 60
            total_minutes = hours_in_minutes + (minutes_offset if hours_in_minutes >= 0 else -minutes_offset)
        except Exception:
            raise ValueError("Offset is too large")
        # Validate minutes component after normalization: it must be within -59..59 relative to hour
        if abs(minutes_offset) > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Ensure total minutes within allowed range
        max_minutes = 23 * 60 + 59
        if total_minutes < -max_minutes or total_minutes > max_minutes:
            raise ValueError("Hours and minutes offset combined out of range")
        try:
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
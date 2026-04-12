    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed-offset time zone from the given hour and minute components.
        """
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        # Calculate total minutes, preserving sign.
        total_minutes = hours_offset * 60 + (minutes_offset if hours_offset >= 0 else -minutes_offset)
        # Convert to milliseconds, checking for overflow.
        try:
            offset = total_minutes * 60 * 1000
        except OverflowError:
            raise ValueError(f"Offset too large: {hours_offset}:{minutes_offset}")
        # Ensure offset is within valid range.
        if offset < -12 * 60 * 60 * 1000 or offset > 12 * 60 * 60 * 1000:
            raise ValueError(f"Offset out of range: {hours_offset}:{minutes_offset}")
        return cls.for_offset_millis(offset)
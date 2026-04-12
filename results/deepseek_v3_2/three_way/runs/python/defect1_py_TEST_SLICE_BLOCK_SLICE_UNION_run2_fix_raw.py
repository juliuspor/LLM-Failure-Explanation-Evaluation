    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed-offset time zone with the given hour and minute offsets.

        Args:
            hours_offset: The hour offset from UTC, between -23 and 23.
            minutes_offset: The minute offset from UTC, between 0 and 59.

        Returns:
            A DateTimeZone with the specified fixed offset.

        Raises:
            ValueError: If the offsets are out of range.
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        offset = total_minutes * 60 * 1000
        return cls.for_offset_millis(offset)
    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours and minutes.
        This method assumes 60 minutes per hour.

        Args:
            hours_offset: the offset in hours, from -23 to +23
            minutes_offset: the offset in minutes, from -59 to +59

        Returns:
            the DateTimeZone object for the offset

        Raises:
            ValueError: if the values are out of range
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        total_millis = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        return cls.for_offset_millis(total_millis)
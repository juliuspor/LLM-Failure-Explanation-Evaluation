    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed-offset time zone from hour and minute components.

        Args:
            hours_offset: Offset in hours, from -23 to 23.
            minutes_offset: Offset in minutes, from -59 to 59. Must have the same sign as hours_offset unless hours_offset is zero.

        Returns:
            A DateTimeZone instance with the specified fixed offset.

        Raises:
            ValueError: If the offset values are out of range or inconsistent.
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        if hours_offset == 0:
            if minutes_offset < 0:
                sign = -1
            else:
                sign = 1
        else:
            if (hours_offset > 0 and minutes_offset < 0) or (hours_offset < 0 and minutes_offset > 0):
                raise ValueError("Minutes offset must have same sign as hours offset")
            sign = 1 if hours_offset > 0 else -1
        total_minutes = abs(hours_offset) * 60 + abs(minutes_offset)
        if total_minutes > 23 * 60 + 59:
            raise ValueError(f"Total offset out of range: {hours_offset}:{minutes_offset}")
        offset_millis = sign * total_minutes * 60 * 1000
        return cls.for_offset_millis(offset_millis)
    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed-offset time zone for the given UTC offset.

        Args:
            hours_offset: Hours offset from UTC (-23 to 23).
            minutes_offset: Minutes offset (0 to 59).

        Returns:
            A DateTimeZone instance with the specified offset.
        """
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        offset = 0
        try:
            hours_in_minutes = hours_offset * 60
            if hours_offset < 0:
                total_minutes = hours_in_minutes - minutes_offset
            else:
                total_minutes = hours_in_minutes + minutes_offset
            offset = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
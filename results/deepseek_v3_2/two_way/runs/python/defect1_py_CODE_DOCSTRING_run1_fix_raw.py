    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed-offset time zone for the given UTC offset.

        The offset is provided as an hours component plus a minutes component and
        is converted to a millisecond offset for the resulting `DateTimeZone`.

        Args:
            hours_offset: Offset in hours relative to UTC (-23 to +23).
            minutes_offset: Offset minutes component (within a single hour).
            
        Returns:
            A `DateTimeZone` instance representing the requested fixed offset.
            
        Raises:
            ValueError: If the provided values are out of range or the resulting offset
                is not supported.
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
            minutes_offset_total = hours_in_minutes + minutes_offset
            offset = FieldUtils.safe_multiply(minutes_offset_total, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
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
            # Convert hours to minutes and combine with minutes_offset.
            # The sign of minutes_offset must be consistent with hours_offset.
            # If hours_offset is negative, minutes_offset should be negative or zero.
            # If hours_offset is positive, minutes_offset should be positive or zero.
            # However, the method allows any sign combination? The test expects mixed signs to be invalid.
            # Actually, the method should treat minutes_offset as an absolute magnitude within 0-59,
            # and the sign of the total offset is determined solely by hours_offset.
            # But the Joda-Time spec says minutes_offset can be negative? The test expects ValueError for mixed signs.
            # Let's re-examine: The bug diagnosis says the test expects mixed signs invalid.
            # The current code does not enforce sign consistency; it just does arithmetic.
            # The fix should ensure that minutes_offset must have the same sign as hours_offset when non-zero,
            # or be zero. This matches Joda-Time behavior.
            if hours_offset > 0 and minutes_offset < 0:
                raise ValueError("Minutes offset must be positive when hours offset is positive")
            if hours_offset < 0 and minutes_offset > 0:
                raise ValueError("Minutes offset must be negative when hours offset is negative")
            # Now compute total minutes.
            total_minutes = hours_offset * 60 + minutes_offset
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
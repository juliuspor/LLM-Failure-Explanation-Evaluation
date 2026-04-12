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
        # Validate minutes based on hours
        if hours_offset != 0:
            # When hours is non-zero, minutes must be 0-59
            if minutes_offset < 0 or minutes_offset > 59:
                raise ValueError(f"Minutes out of range: {minutes_offset}")
        else:
            # When hours is zero, minutes can be -59..59 but not zero (already handled)
            if minutes_offset < -59 or minutes_offset > 59:
                raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Compute total minutes
        total_minutes = hours_offset * 60 + minutes_offset
        try:
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
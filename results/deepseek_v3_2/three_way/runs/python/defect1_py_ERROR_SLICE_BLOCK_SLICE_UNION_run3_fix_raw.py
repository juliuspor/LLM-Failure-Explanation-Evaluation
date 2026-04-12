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
        # minutes_offset must be between 0 and 59 inclusive, regardless of sign of hours_offset.
        # The sign of the offset is determined by hours_offset, so minutes_offset should be non-negative.
        # However, the user might pass a negative minutes_offset? The spec says minutes_offset is a component.
        # We should treat minutes_offset as magnitude, so we take its absolute value.
        # But the original code allowed negative minutes_offset? Actually the validation rejects negative.
        # The bug is that minutes_offset becomes negative due to calculation earlier.
        # Let's adjust: we should compute total minutes without modifying minutes_offset.
        # Actually, the bug is in the calculation: we are modifying minutes_offset incorrectly.
        # Let's re-examine the original code:
        #   hours_in_minutes = hours_offset * 60
        #   if hours_in_minutes < 0:
        #       minutes_offset = hours_in_minutes - minutes_offset
        #   else:
        #       minutes_offset = hours_in_minutes + minutes_offset
        # This is wrong because it changes the sign of minutes_offset incorrectly.
        # The correct approach: total_minutes = hours_offset * 60 + minutes_offset
        # But minutes_offset can be negative? The spec says minutes_offset is within a single hour.
        # Typically minutes_offset is non-negative (0-59). However, to allow negative offsets like -05:30,
        # we need to allow minutes_offset to be negative? Actually, the offset sign is determined by hours_offset.
        # For example, -05:30 means hours_offset = -5, minutes_offset = 30 (positive).
        # So minutes_offset should be non-negative, and the sign is from hours_offset.
        # Therefore, we should validate minutes_offset as 0-59.
        # But the bug diagnosis says minutes_offset becomes -15. That's because the calculation above sets it to negative.
        # So we need to fix the calculation.
        # Let's rewrite:
        #   total_minutes = hours_offset * 60 + minutes_offset
        # But we must ensure minutes_offset is non-negative.
        # However, if hours_offset is negative and minutes_offset is positive, total_minutes will be negative.
        # That's fine.
        # So we should not modify minutes_offset variable; instead compute total_minutes.
        # And we should validate minutes_offset as 0-59.
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        offset = 0
        try:
            total_minutes = hours_offset * 60 + minutes_offset
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
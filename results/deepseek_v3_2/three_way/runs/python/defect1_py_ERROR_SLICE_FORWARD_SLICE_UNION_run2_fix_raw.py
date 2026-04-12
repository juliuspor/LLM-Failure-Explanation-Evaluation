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
        # Allow minutes_offset to be negative only if hours_offset is zero? Actually, minutes_offset should be within -59..59.
        # But the method expects minutes within an hour. However, the bug is that the validation is too strict.
        # The specification says minutes_offset is offset minutes component (within a single hour).
        # That implies absolute value should be 0-59. But the bug report shows minutes_offset = -15.
        # That's invalid per spec, but the code later tries to adjust minutes_offset based on hours_in_minutes.
        # Actually, the logic is flawed: the method should accept negative minutes_offset only when hours_offset is negative?
        # Let's examine the original logic: they compute hours_in_minutes = hours_offset * 60.
        # Then if hours_in_minutes < 0, they do minutes_offset = hours_in_minutes - minutes_offset.
        # else minutes_offset = hours_in_minutes + minutes_offset.
        # This suggests that minutes_offset is meant to be a signed component? Actually, the parameter is called minutes_offset.
        # It could be positive or negative? The spec says "offset minutes component (within a single hour)".
        # That could be interpreted as the minutes part of the offset, which could be negative if the total offset is negative.
        # For example, offset -05:30 would have hours_offset = -5, minutes_offset = -30.
        # But the validation minutes_offset < 0 or minutes_offset > 59 would reject -30.
        # So the fix is to allow minutes_offset in range -59..59.
        # However, we must also ensure that the total minutes offset is within - (23*60 + 59) to (23*60 + 59).
        # Let's adjust validation: allow minutes_offset between -59 and 59 inclusive.
        # But also need to ensure that the sign of minutes_offset matches hours_offset? Not necessarily.
        # For example, hours_offset = 1, minutes_offset = -30 would give total minutes = 30, which is fine.
        # The original code would compute hours_in_minutes = 60, then minutes_offset = 60 + (-30) = 30.
        # That works. So we can allow minutes_offset in -59..59.
        # However, we must also ensure that the total minutes offset is within - (23*60 + 59) to (23*60 + 59).
        # That will be caught by the safe_multiply and the final offset validation in for_offset_millis.
        # So fix: change validation to allow -59 to 59.
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        offset = 0
        try:
            hours_in_minutes = hours_offset * 60
            if hours_in_minutes < 0:
                minutes_offset = hours_in_minutes - minutes_offset
            else:
                minutes_offset = hours_in_minutes + minutes_offset
            offset = FieldUtils.safe_multiply(minutes_offset, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
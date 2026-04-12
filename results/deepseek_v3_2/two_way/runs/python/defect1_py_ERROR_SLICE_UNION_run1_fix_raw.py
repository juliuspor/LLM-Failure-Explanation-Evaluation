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
        # minutes_offset can be negative? Actually, the parameter minutes_offset is the minutes component,
        # which should be between 0 and 59. However, the bug diagnosis says minutes_offset becomes -15.
        # That's because the original code allowed negative minutes_offset? Wait, the parameter is minutes_offset.
        # The bug is that the code later modifies minutes_offset, but the range check is done before that modification.
        # Actually, the range check should be on the absolute value of minutes_offset? No, minutes_offset should be non-negative.
        # The spec says minutes_offset is within a single hour, so 0-59. But the user might pass negative minutes? 
        # The function should reject negative minutes_offset. However, the bug diagnosis says minutes_offset is -15 after calculation.
        # That suggests the calculation is wrong. Let's examine the original code:
        # hours_in_minutes = hours_offset * 60
        # if hours_in_minutes < 0:
        #     minutes_offset = hours_in_minutes - minutes_offset
        # else:
        #     minutes_offset = hours_in_minutes + minutes_offset
        # This is trying to compute total minutes offset, but it's incorrectly using the original minutes_offset.
        # Actually, the goal is to compute total minutes offset = hours_offset * 60 + minutes_offset.
        # But the code does: if hours_in_minutes < 0: minutes_offset = hours_in_minutes - minutes_offset
        # That would be hours_offset*60 - minutes_offset, which is wrong.
        # The correct formula is total_minutes = hours_offset * 60 + minutes_offset.
        # However, note that minutes_offset parameter is always non-negative? The spec says minutes component.
        # But the function might be called with negative minutes_offset? The bug diagnosis says minutes_offset becomes -15.
        # That's because the original code allowed negative minutes_offset? Actually, the range check is after the calculation? No, the range check is before.
        # Wait, the bug diagnosis says: "The condition `if minutes_offset < 0 or minutes_offset > 59:` triggers a ValueError because `minutes_offset` is less than 0."
        # That means the parameter minutes_offset is -15. So the user passed -15. But the spec says minutes_offset is within a single hour, so should be 0-59.
        # However, the function might be used to create offsets like +05:-15? That's not standard. But the function should handle negative minutes_offset? 
        # Actually, the function is for_offset_hours_minutes, and the minutes_offset is the minutes component, which could be negative if the offset is negative?
        # But typically, offsets are expressed as +HH:MM or -HH:MM, where MM is always positive. So -05:15 means offset -5 hours and -15 minutes? Actually, -05:15 means offset = -5 hours -15 minutes = -315 minutes.
        # So minutes_offset should be allowed to be negative? The spec says "Offset minutes component (within a single hour)." That implies absolute value less than 60, but sign? Usually, the sign is determined by hours_offset.
        # However, the function signature doesn't enforce that minutes_offset has the same sign as hours_offset. The user could pass hours_offset=5, minutes_offset=-15, which would be weird.
        # The original code from Joda-Time? In Joda-Time, forOffsetHoursMinutes(int hoursOffset, int minutesOffset) expects minutesOffset to be between -59 and 59, and the sign must be the same as hoursOffset if hoursOffset is non-zero.
        # Actually, looking at Joda-Time source: they have a check: if (hoursOffset < -23 || hoursOffset > 23) ...
        # if (minutesOffset < -59 || minutesOffset > 59) ...
        # and then: if (hoursOffset > 0 && minutesOffset < 0) ... if (hoursOffset < 0 && minutesOffset > 0) ...
        # So minutesOffset can be negative. The bug is that the range check in our code is wrong: it should allow negative minutes.
        # But the bug diagnosis says minutes_offset is -15, which is within -59..59, so the range check should pass. However, our range check is minutes_offset < 0 or minutes_offset > 59, which rejects negative.
        # So we need to change the range check to allow -59 to 59.
        # Also, we need to ensure that the sign of minutes_offset matches hours_offset. Let's adopt Joda-Time's logic.
        # Steps:
        # 1. Check hours_offset range -23..23.
        # 2. Check minutes_offset range -59..59.
        # 3. If hours_offset > 0 and minutes_offset < 0, raise error.
        # 4. If hours_offset < 0 and minutes_offset > 0, raise error.
        # 5. Compute total minutes = hours_offset * 60 + minutes_offset.
        # 6. Convert to millis and call for_offset_millis.
        # Let's implement that.
        
        # Check ranges
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Check sign consistency
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError(f"Positive hours offset {hours_offset} but negative minutes offset {minutes_offset}")
        if hours_offset < 0 and minutes_offset > 0:
            raise ValueError(f"Negative hours offset {hours_offset} but positive minutes offset {minutes_offset}")
        # Compute total minutes
        total_minutes = hours_offset * 60 + minutes_offset
        # Convert to millis
        try:
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
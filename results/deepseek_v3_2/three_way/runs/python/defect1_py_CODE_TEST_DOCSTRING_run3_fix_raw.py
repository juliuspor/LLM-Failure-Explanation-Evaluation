    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Ensure consistent signs: if hours_offset is negative, minutes_offset must be non-negative.
        # Actually, the spec says minutes_offset is within a single hour (0-59).
        # So we should not allow negative minutes_offset at all.
        # But the bug diagnosis mentions that minutes_offset can be negative when hours_offset is negative?
        # However, the docstring says minutes_offset is "Offset minutes component (within a single hour)."
        # That implies 0-59. The test expects ValueError for (2, -15) and no error for (-2, 15).
        # So we should keep the minutes range check as above (0-59).
        # The bug is in the calculation when hours_offset is negative.
        # We need to compute total minutes correctly.
        # total_minutes = hours_offset * 60 + minutes_offset
        # But we must be careful with signs.
        # Let's compute directly:
        total_minutes = hours_offset * 60 + minutes_offset
        # Now total_minutes could be negative, but that's fine.
        # However, we must ensure that total_minutes is within -23*60 to +23*60.
        # Actually, the range of total_minutes should be between - (23*60 + 59) and + (23*60 + 59).
        # But we already checked hours_offset and minutes_offset individually.
        # The combined offset must be within -23:59 and +23:59.
        # Since hours_offset is within -23..23 and minutes_offset within 0..59, total_minutes is automatically within range.
        # However, we need to ensure that the total offset in milliseconds does not overflow.
        # Use safe_multiply.
        try:
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
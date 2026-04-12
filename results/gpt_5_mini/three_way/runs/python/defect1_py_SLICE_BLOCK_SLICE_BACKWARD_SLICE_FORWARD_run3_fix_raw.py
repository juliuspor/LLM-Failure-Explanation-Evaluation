@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        # Normalize minutes_offset so that its sign matches hours_offset and is within 0..59
        # Allow callers to pass negative minutes_offset or values >=60
        # Compute total minutes as hours_offset * 60 + sign(minutes_offset) * abs(minutes_offset)
        # But handle cases where minutes_offset may have its own sign
        # Convert combined total minutes then validate hours range
        # First, convert inputs to total minutes
        total_minutes = hours_offset * 60 + minutes_offset
        # Now derive normalized hours and minutes for validation of hours range
        norm_hours = total_minutes // 60
        norm_minutes = abs(total_minutes % 60)
        # If total_minutes negative and not divisible by 60, adjust representation so minutes positive
        if total_minutes < 0 and total_minutes % 60 != 0:
            # e.g., total_minutes = -30 --> norm_hours = -1, norm_minutes = 30 should represent -0:30 -> -0 hours and -30 minutes? Keep total_minutes as authoritative
            # Keep norm_hours as floor div already does the right thing for range check
            pass
        if norm_hours < -23 or norm_hours > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        # Recompute total_minutes to ensure consistency (already correct)
        try:
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
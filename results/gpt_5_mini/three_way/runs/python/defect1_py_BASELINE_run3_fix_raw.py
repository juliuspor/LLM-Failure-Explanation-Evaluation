@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Disallow mixing signs: hours and minutes must have same sign, unless one is zero
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError("Hours and minutes must have the same sign")
        if hours_offset < 0 and minutes_offset > 0:
            raise ValueError("Hours and minutes must have the same sign")
        try:
            # Compute total minutes taking sign into account
            total_minutes = hours_offset * 60 + (minutes_offset if hours_offset >= 0 else -abs(minutes_offset) if hours_offset < 0 else minutes_offset)
            # The above ensures that when hours_offset is negative, minutes_offset contributes negatively.
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
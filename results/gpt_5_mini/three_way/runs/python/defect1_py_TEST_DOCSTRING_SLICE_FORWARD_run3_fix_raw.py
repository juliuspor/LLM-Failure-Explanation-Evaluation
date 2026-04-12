@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Reject mixed sign inputs like (2, -15) or (-2, 15) should be allowed if minutes sign matches hours sign
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError("Hours and minutes must have the same sign")
        if hours_offset < 0 and minutes_offset > 0:
            # allow (-2, 15) meaning -2 hours and -15 minutes -> total negative
            pass
        # Determine total minutes correctly respecting sign
        try:
            total_minutes = hours_offset * 60
            # If hours_offset is negative, minutes_offset should be subtracted (i.e. more negative)
            if hours_offset < 0:
                total_minutes -= abs(minutes_offset)
            else:
                total_minutes += abs(minutes_offset)
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
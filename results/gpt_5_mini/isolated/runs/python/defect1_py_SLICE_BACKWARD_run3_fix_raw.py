@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        # Ensure minutes_offset is an int and within 0..59
        try:
            if not isinstance(minutes_offset, int):
                minutes_offset = int(minutes_offset)
        except (TypeError, ValueError):
            raise ValueError(f"Minutes value is not a valid integer: {minutes_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        try:
            # compute total minutes taking into account sign of hours
            total_minutes = hours_offset * 60
            if total_minutes < 0:
                total_minutes -= minutes_offset
            else:
                total_minutes += minutes_offset
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
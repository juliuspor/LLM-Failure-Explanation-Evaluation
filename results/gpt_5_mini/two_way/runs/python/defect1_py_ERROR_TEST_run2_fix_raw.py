@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        # Allow minutes to be negative when hours is negative, or positive when hours is positive.
        # Also allow negative minutes when hours is zero (to represent offsets like -00:15).
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Combine hours and minutes into total minutes
        try:
            total_minutes = hours_offset * 60
            # If hours and minutes have opposite signs, normalize by applying the sign of hours
            if hours_offset > 0 and minutes_offset < 0:
                # e.g., +1 hour and -15 minutes -> +45 minutes
                total_minutes += minutes_offset
            elif hours_offset < 0 and minutes_offset > 0:
                # e.g., -1 hour and +15 minutes -> -45 minutes
                total_minutes -= minutes_offset
            else:
                # same sign or hours == 0
                total_minutes += minutes_offset
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
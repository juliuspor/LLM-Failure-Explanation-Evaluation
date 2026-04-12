@classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        # minutes_offset may be negative to indicate negative offsets like -02:15
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        try:
            total_minutes = hours_offset * 60 + (minutes_offset if hours_offset >= 0 else -abs(minutes_offset))
            # Validate resulting hours range after combining minutes
            hours_part = total_minutes // 60
            mins_part = abs(total_minutes % 60)
            if hours_part < -23 or hours_part > 23 or mins_part < 0 or mins_part > 59:
                raise ValueError(f"Invalid offset hours/minutes combination: {hours_offset}, {minutes_offset}")
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        if total_minutes < -23 * 60 or total_minutes > 23 * 60:
            raise ValueError(f"Total offset out of range: {hours_offset}:{minutes_offset}")
        if minutes_offset % 1 != 0:
            raise ValueError(f"Minutes must be integer: {minutes_offset}")
        offset = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        if offset < -cls._MAX_MILLIS or offset > cls._MAX_MILLIS:
            raise ValueError(f"Offset out of range: {hours_offset}:{minutes_offset}")
        return cls.for_offset_millis(offset)
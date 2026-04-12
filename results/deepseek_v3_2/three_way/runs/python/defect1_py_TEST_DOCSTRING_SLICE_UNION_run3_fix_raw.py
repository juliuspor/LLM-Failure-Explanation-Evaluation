    @classmethod
    def for_offset(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        offset_millis = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        return cls.for_offset_millis(offset_millis)
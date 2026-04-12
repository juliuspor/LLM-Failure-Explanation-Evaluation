    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        total_minutes = hours_offset * 60
        if hours_offset >= 0:
            total_minutes += minutes_offset
        else:
            total_minutes -= minutes_offset
        total_millis = total_minutes * 60000
        return cls.for_offset_millis(total_millis)
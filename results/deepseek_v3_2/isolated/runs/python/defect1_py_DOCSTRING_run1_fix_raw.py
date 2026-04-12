    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        offset_millis = (hours_offset * 60 + minutes_offset) * 60 * 1000
        zone_id = cls._print_offset(offset_millis)
        return FixedDateTimeZone(zone_id, None, offset_millis, offset_millis)
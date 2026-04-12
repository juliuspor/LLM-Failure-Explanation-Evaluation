    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        if hours_offset < 0 and minutes_offset > 0:
            raise ValueError(f"Minutes must be negative when hours are negative: {minutes_offset}")
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError(f"Minutes must be positive when hours are positive: {minutes_offset}")
        offset = hours_offset * 3600000 + minutes_offset * 60000
        if offset == 0:
            return cls.UTC
        else:
            zone_id = cls._print_offset(offset)
            return cls._fixed_offset_zone(zone_id, offset)

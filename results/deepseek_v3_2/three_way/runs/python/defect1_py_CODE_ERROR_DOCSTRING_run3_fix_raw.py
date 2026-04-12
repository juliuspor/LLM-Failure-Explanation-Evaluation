    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        try:
            offset = FieldUtils.safeMultiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError(f"Total offset out of range: {total_minutes} minutes")
        zone_id = cls._print_offset(offset)
        return cls._fixed_offset_zone(zone_id, offset)
    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed-offset time zone with the given hour and minute offset.
        
        Args:
            hours_offset: the offset in hours, can be negative
            minutes_offset: the offset in minutes, must be between 0 and 59
        
        Returns:
            the DateTimeZone object
        """
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError("Hours offset must be in range -23 to 23")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError("Minutes offset must be in range 0 to 59")
        total_minutes = hours_offset * 60 + minutes_offset
        offset_millis = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        zone_id = cls._print_offset(offset_millis)
        return FixedDateTimeZone(zone_id, None, offset_millis, offset_millis)
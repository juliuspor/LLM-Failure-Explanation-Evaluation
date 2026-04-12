    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed time zone with the specified hour and minute offset.
        
        Args:
            hours_offset: The hour offset from UTC (-23 to 23).
            minutes_offset: The minute offset from UTC (0 to 59).
            
        Returns:
            A DateTimeZone instance with the given offset.
            
        Raises:
            ValueError: If the offset values are out of range.
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        total_minutes = hours_offset * 60 + minutes_offset
        offset_millis = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        zone_id = cls._print_offset(offset_millis)
        return cls._fixed_offset_zone(zone_id, offset_millis)
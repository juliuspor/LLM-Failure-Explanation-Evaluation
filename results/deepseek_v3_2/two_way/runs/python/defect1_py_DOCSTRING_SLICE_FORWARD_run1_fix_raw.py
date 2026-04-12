    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone for the specified offset to UTC in hours and minutes.
        
        This method accepts offsets from -23:59 to +23:59.
        
        Args:
            hours_offset: the offset in hours, from -23 to 23
            minutes_offset: the offset in minutes, from 0 to 59
        
        Returns:
            the DateTimeZone object for the offset
        
        Raises:
            ValueError: if the offset is out of range
        """
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError("Hours offset out of range: " + str(hours_offset))
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError("Minutes offset out of range: " + str(minutes_offset))
        total_minutes = hours_offset * 60 + minutes_offset
        offset = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        zone_id = cls._print_offset(offset)
        return cls._fixed_offset_zone(zone_id, offset)
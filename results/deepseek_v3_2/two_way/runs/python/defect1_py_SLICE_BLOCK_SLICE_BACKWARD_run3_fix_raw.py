    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Returns a time zone instance for the specified offset to UTC in hours and minutes.
        
        Args:
            hours_offset: the offset in hours, from -23 to 23
            minutes_offset: the offset in minutes, from 0 to 59
            
        Returns:
            the DateTimeZone
            
        Raises:
            ValueError: if the offset is out of range
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError("Hours offset must be in the range -23 to 23")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError("Minutes offset must be in the range 0 to 59")
        if hours_offset > 0 and minutes_offset < 0:
            minutes_offset = -minutes_offset
        elif hours_offset < 0 and minutes_offset > 0:
            minutes_offset = -minutes_offset
        total_offset = hours_offset * DateTimeConstants.MILLIS_PER_HOUR + minutes_offset * DateTimeConstants.MILLIS_PER_MINUTE
        return cls.for_offset_millis(total_offset)
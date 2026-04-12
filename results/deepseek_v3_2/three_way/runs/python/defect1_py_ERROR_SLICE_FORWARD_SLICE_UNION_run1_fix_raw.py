    @classmethod
    def for_offset_hours(cls, hours_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset in hours.
        
        Args:
            hours_offset: the offset in hours from UTC, from -23 to +23
            
        Returns:
            the DateTimeZone object for the offset
        """
        return cls.for_offset_hours_minutes(hours_offset, 0)
    
    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed-offset time zone for the given UTC offset.
        
        Args:
            hours_offset: hours component of offset (-23 to 23)
            minutes_offset: minutes component of offset (0 to 59)
            
        Returns:
            DateTimeZone instance with the specified offset
            
        Raises:
            ValueError: if offset values are out of range
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        
        total_minutes = hours_offset * 60 + minutes_offset
        if total_minutes < -1439 or total_minutes > 1439:
            raise ValueError(f"Total offset out of range: {total_minutes} minutes")
        
        offset_millis = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        return cls.for_offset_millis(offset_millis)
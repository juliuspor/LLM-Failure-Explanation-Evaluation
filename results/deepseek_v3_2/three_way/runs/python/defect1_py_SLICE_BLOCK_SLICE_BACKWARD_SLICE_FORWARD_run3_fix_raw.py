    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours and minutes.
        This method assumes 60 minutes per hour, and that hours and minutes are within the valid range.
        The offset must be within the range -23:59 to +23:59.
        
        Args:
            hours_offset: the offset in hours, from -23 to 23.
            minutes_offset: the offset in minutes, from 0 to 59.
        
        Returns:
            the DateTimeZone object for the offset.
        
        Raises:
            ValueError: if the offset is out of range.
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError("Hours offset must be in range -23 to 23")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError("Minutes offset must be in range 0 to 59")
        if hours_offset > 0 and minutes_offset < 0:
            raise ValueError("Positive offset must have positive minutes")
        if hours_offset < 0 and minutes_offset > 0:
            raise ValueError("Negative offset must have negative minutes")
        total_minutes = hours_offset * 60 + minutes_offset
        if total_minutes < -23 * 60 or total_minutes > 23 * 60:
            raise ValueError("Total offset must be in range -23:59 to +23:59")
        return cls.for_offset_minutes(total_minutes)
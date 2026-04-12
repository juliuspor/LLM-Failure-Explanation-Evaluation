    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours and minutes.
        This method assumes 60 minutes in an hour, and that the sign of hours and minutes is the same.
        
        Args:
            hours_offset: the offset in hours, from -23 to 23
            minutes_offset: the offset in minutes, from 0 to 59
            
        Returns:
            the DateTimeZone object
            
        Raises:
            ValueError: if the offset is too large or the signs differ
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError("Hours offset out of range: " + str(hours_offset))
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError("Minutes offset out of range: " + str(minutes_offset))
        if (hours_offset < 0 and minutes_offset > 0) or (hours_offset > 0 and minutes_offset < 0):
            raise ValueError("Hours and minutes offset signs must match")
        offset = hours_offset * 60 + minutes_offset
        if offset < -23 * 60 or offset > 23 * 60:
            raise ValueError("Offset is too large")
        return cls.for_offset_minutes(offset)
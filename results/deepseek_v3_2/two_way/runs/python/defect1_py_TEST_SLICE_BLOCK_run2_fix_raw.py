    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed offset time zone from hours and minutes.
        
        Args:
            hours_offset: Offset in hours (-23 to 23).
            minutes_offset: Offset in minutes (-59 to 59).
            
        Returns:
            DateTimeZone: A fixed offset time zone.
            
        Raises:
            ValueError: If the offset is out of range.
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        offset = total_minutes * 60000
        return cls.for_offset_millis(offset)
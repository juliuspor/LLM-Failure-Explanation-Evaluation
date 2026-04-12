    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Returns a time zone with a fixed offset from UTC.
        
        Args:
            hours_offset: the offset in hours, from -23 to 23
            minutes_offset: the offset in minutes, from 0 to 59
        
        Returns:
            a DateTimeZone with the specified fixed offset
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        offset_millis = total_minutes * 60000
        return cls.for_offset_millis(offset_millis)
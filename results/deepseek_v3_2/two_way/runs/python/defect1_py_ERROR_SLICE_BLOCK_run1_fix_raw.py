    @classmethod
    def for_offset(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Create a fixed offset time zone from hours and minutes.
        
        Args:
            hours_offset: the offset in hours, from -23 to 23.
            minutes_offset: the offset in minutes, from -59 to 59.
        
        Returns:
            a fixed offset time zone.
        """
        total_minutes = hours_offset * 60 + minutes_offset
        if total_minutes < -23 * 60 or total_minutes > 23 * 60:
            raise ValueError(f"Total offset out of range: {total_minutes} minutes")
        offset_ms = total_minutes * 60 * 1000
        return cls.for_offset_ms(offset_ms)
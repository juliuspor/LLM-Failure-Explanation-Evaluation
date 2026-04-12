    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours and minutes.
        This method allows combinations of signs, such as +2 and -15.
        
        Args:
            hours_offset: the offset in hours, from -23 to 23
            minutes_offset: the offset in minutes, from -59 to 59
        
        Returns:
            the DateTimeZone object for the offset
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        offset_millis = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        if offset_millis == 0:
            return cls.UTC
        zone_id = cls._print_offset(offset_millis)
        return cls._fixed_offset_zone(zone_id, offset_millis)
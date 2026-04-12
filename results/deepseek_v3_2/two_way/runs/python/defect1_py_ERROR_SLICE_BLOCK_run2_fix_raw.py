    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours and minutes.
        
        This factory is a convenient way to construct zones with a fixed offset.
        
        Args:
            hours_offset: the offset in hours from UTC, from -23 to 23
            minutes_offset: the offset minutes, from 0 to 59
            
        Returns:
            the DateTimeZone object for the offset
        """
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < 0 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        return cls.for_offset_millis(offset)
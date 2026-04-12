    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified UTC offset.
        
        Args:
            hours_offset: the offset in hours from UTC
            minutes_offset: the offset in minutes from UTC, from 0 to 59
            
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
        if total_minutes < -23*60 or total_minutes > 23*60:
            raise ValueError(f"Total minutes out of range: {total_minutes}")
        try:
            offset = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        except ArithmeticError:
            raise ValueError(f"Offset out of range: {total_minutes}")
        return cls.for_offset_millis(offset)
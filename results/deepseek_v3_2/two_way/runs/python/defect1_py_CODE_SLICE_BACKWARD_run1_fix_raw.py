    @classmethod
    def for_offset_hours_minutes(cls, hours: int, minutes: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours and minutes.
        This is a convenience method that constructs a time zone with a fixed offset.
        
        Args:
            hours: the offset in hours, from -23 to 23
            minutes: the offset in minutes, from 0 to 59
            
        Returns:
            the DateTimeZone object for the offset
        """
        if not (-23 <= hours <= 23):
            raise ValueError("Hours out of range: " + str(hours))
        if not (0 <= minutes <= 59):
            raise ValueError("Minutes out of range: " + str(minutes))
        total_minutes = hours * 60 + minutes
        try:
            offset = FieldUtils.safe_multiply(total_minutes, DateTimeConstants.MILLIS_PER_MINUTE)
        except ArithmeticError:
            raise ValueError("Offset is too large")
        return cls.for_offset_millis(offset)
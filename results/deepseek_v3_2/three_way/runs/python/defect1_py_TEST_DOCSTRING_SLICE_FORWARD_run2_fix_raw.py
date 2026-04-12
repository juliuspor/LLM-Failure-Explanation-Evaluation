    @classmethod
    def for_offset_hours_minutes(cls, hours: int, minutes: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours and minutes.
        This method assumes 60 minutes per hour, and that hours and minutes have the same sign.
        
        Args:
            hours: the offset in hours, from -23 to 23
            minutes: the offset in minutes, from -59 to 59
            
        Returns:
            the DateTimeZone
            
        Raises:
            ValueError: if the offset is out of range or hours and minutes have different signs
        """
        if hours < -23 or hours > 23:
            raise ValueError(f"Hours out of range: {hours}")
        if minutes < -59 or minutes > 59:
            raise ValueError(f"Minutes out of range: {minutes}")
        if hours == 0:
            # minutes can be any sign, but must be within range
            pass
        else:
            # hours and minutes must have same sign
            if (hours > 0 and minutes < 0) or (hours < 0 and minutes > 0):
                raise ValueError(f"Hours and minutes must have the same sign: hours={hours}, minutes={minutes}")
        total_minutes = hours * 60 + minutes
        offset_millis = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        return cls.for_offset_millis(offset_millis)
    @classmethod
    def for_offset(cls, offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in milliseconds.
        
        Args:
            offset: the offset in milliseconds from UTC
            
        Returns:
            the DateTimeZone
        """
        if offset < -12 * 60 * 60 * 1000 or offset > 12 * 60 * 60 * 1000:
            raise ValueError("Offset out of range: " + str(offset))
        return cls._for_offset(offset)

    @classmethod
    def _for_offset(cls, offset: int) -> 'DateTimeZone':
        """
        Private method to get a time zone for the offset.
        """
        # Use a simple fixed offset zone
        return FixedDateTimeZone(offset)

    @classmethod
    def for_offset_hours_minutes(cls, hours: int, minutes: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours and minutes.
        
        Args:
            hours: the offset in hours from UTC, range -12 to 12
            minutes: the offset in minutes from UTC, range 0 to 59
            
        Returns:
            the DateTimeZone
        """
        if hours < -12 or hours > 12:
            raise ValueError("Hours out of range: " + str(hours))
        if minutes < 0 or minutes > 59:
            raise ValueError("Minutes out of range: " + str(minutes))
        if hours < 0:
            minutes = -minutes
        total_minutes = hours * 60 + minutes
        offset = total_minutes * 60 * 1000
        return cls._for_offset(offset)
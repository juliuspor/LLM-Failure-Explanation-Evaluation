    @classmethod
    def for_offset_millis(cls, offset: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in milliseconds.
        
        Args:
            offset: the offset in millis from UTC
            
        Returns:
            the time zone instance
        """
        if offset == 0:
            return cls.UTC
        # Build a string representation of the offset
        total_minutes = offset // DateTimeConstants.MILLIS_PER_MINUTE
        hours = total_minutes // 60
        minutes = total_minutes % 60
        seconds = (offset % DateTimeConstants.MILLIS_PER_MINUTE) // DateTimeConstants.MILLIS_PER_SECOND
        millis = offset % DateTimeConstants.MILLIS_PER_SECOND
        parts = []
        if hours < 0 or minutes < 0 or seconds < 0 or millis < 0:
            parts.append('-')
            hours = -hours
            minutes = -minutes
            seconds = -seconds
            millis = -millis
        else:
            parts.append('+')
        parts.append(f'{hours:02d}:{minutes:02d}')
        if seconds != 0 or millis != 0:
            parts.append(f':{seconds:02d}')
            if millis != 0:
                parts.append(f'.{millis:03d}')
        zone_id = ''.join(parts)
        return cls._fixed_offset_zone(zone_id, offset)

    @classmethod
    def for_offset_hours_minutes(cls, hours: int, minutes: int) -> 'DateTimeZone':
        """
        Gets a time zone instance for the specified offset to UTC in hours and minutes.
        
        Args:
            hours: the offset in hours from UTC, from -23 to +23
            minutes: the offset in minutes from UTC, from -59 to +59
            
        Returns:
            the time zone instance
        """
        if hours < -23 or hours > 23:
            raise ValueError(f'Hours out of range: {hours}')
        if minutes < -59 or minutes > 59:
            raise ValueError(f'Minutes out of range: {minutes}')
        total_minutes = hours * 60 + minutes
        offset = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        return cls.for_offset_millis(offset)

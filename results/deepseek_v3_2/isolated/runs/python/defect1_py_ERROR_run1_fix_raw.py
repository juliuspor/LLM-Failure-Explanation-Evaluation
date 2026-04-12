    @classmethod
    def for_offset_hours_minutes(cls, hours: int, minutes: int) -> 'DateTimeZone':
        """
        Gets a fixed time zone instance with the specified offset.
        
        Args:
            hours: the offset in hours, from -23 to 23
            minutes: the offset in minutes, from -59 to 59
            
        Returns:
            the DateTimeZone instance
        """
        if hours < -23 or hours > 23:
            raise ValueError(f"Hours out of range: {hours}")
        if minutes < -59 or minutes > 59:
            raise ValueError(f"Minutes out of range: {minutes}")
        if (hours > 0 and minutes < 0) or (hours < 0 and minutes > 0):
            raise ValueError(f"Hours and minutes have inconsistent signs: hours={hours}, minutes={minutes}")
        total_minutes = hours * 60 + minutes
        offset_millis = total_minutes * 60 * 1000
        if offset_millis == 0:
            return cls.UTC
        else:
            zone_id = cls._print_offset(offset_millis)
            return cls._fixed_offset_zone(zone_id, offset_millis)
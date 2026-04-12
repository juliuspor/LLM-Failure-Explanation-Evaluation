    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Gets a fixed offset time zone for the given offset hours and minutes.
        
        Args:
            hours_offset: Offset hours, from -23 to +23.
            minutes_offset: Offset minutes, from -59 to +59. If hours_offset is negative, minutes_offset should also be negative to produce a consistent negative offset.
            
        Returns:
            A DateTimeZone instance with the given fixed offset.
            
        Raises:
            ValueError: If the offset is out of range.
        """
        if hours_offset < -23 or hours_offset > 23:
            raise ValueError(f"Hours out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes out of range: {minutes_offset}")
        # Ensure sign consistency: if hours is negative, minutes should be negative; if hours positive, minutes positive.
        if (hours_offset > 0 and minutes_offset < 0) or (hours_offset < 0 and minutes_offset > 0):
            raise ValueError(f"Inconsistent sign: hours={hours_offset}, minutes={minutes_offset}")
        total_minutes = hours_offset * 60 + minutes_offset
        if total_minutes < -1439 or total_minutes > 1439:
            raise ValueError(f"Total offset out of range: {hours_offset}:{minutes_offset}")
        offset_millis = total_minutes * DateTimeConstants.MILLIS_PER_MINUTE
        zone_id = cls._print_offset(offset_millis)
        return cls._fixed_offset_zone(zone_id, offset_millis)
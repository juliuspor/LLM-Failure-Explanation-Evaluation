    @staticmethod
    def for_offset_hours_minutes(hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Returns a fixed time zone for the given offset hours and minutes.
        
        Args:
            hours_offset: the offset in hours, from -24 to +24
            minutes_offset: the offset minutes component, from -59 to +59.
                Must have the same sign as hours_offset when hours_offset is non-zero.
                If hours_offset is zero, minutes_offset can be positive or negative.
        
        Returns:
            a DateTimeZone with the given fixed offset
        
        Raises:
            ValueError: if the offset is out of range or the signs are inconsistent
        """
        if hours_offset < -24 or hours_offset > 24:
            raise ValueError(f"Hours offset out of range: {hours_offset}")
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValueError(f"Minutes offset out of range: {minutes_offset}")
        if hours_offset == 0:
            if minutes_offset == 0:
                return DateTimeZone.UTC
        else:
            if (hours_offset > 0 and minutes_offset < 0) or (hours_offset < 0 and minutes_offset > 0):
                raise ValueError(
                    f"Hours offset ({hours_offset}) and minutes offset ({minutes_offset}) must have the same sign"
                )
        total_millis = FieldUtils.safe_multiply(hours_offset, DateTimeConstants.MILLIS_PER_HOUR) + \
                       FieldUtils.safe_multiply(minutes_offset, DateTimeConstants.MILLIS_PER_MINUTE)
        if total_millis < -DateTimeConstants.MILLIS_PER_DAY or total_millis > DateTimeConstants.MILLIS_PER_DAY:
            raise ValueError(f"Total offset out of range: {total_millis} ms")
        offset_str = DateTimeZone._print_offset(total_millis)
        return FixedDateTimeZone(offset_str, None, total_millis, total_millis)
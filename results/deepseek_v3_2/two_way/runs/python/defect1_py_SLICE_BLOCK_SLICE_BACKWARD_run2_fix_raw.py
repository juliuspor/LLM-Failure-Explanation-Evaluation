    @classmethod
    def for_offset_hours_minutes(cls, hours: int, minutes: int) -> 'DateTimeZone':
        """
        Creates a fixed offset time zone with the given hours and minutes.
        This is a corrected version of the original method.
        """
        if hours < -23 or hours > 23:
            raise ValueError(f"Hours offset out of range: {hours}")
        if minutes < -59 or minutes > 59:
            raise ValueError(f"Minutes offset out of range: {minutes}")
        total_minutes = hours * 60 + minutes
        total_millis = total_minutes * 60 * 1000
        offset_str = cls._print_offset(total_millis)
        return FixedDateTimeZone(offset_str, None, total_millis, total_millis)
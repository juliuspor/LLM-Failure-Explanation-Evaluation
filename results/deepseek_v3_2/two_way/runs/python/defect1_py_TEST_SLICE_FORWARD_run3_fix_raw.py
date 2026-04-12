    @classmethod
    def for_offset_hours_minutes(cls, hours_offset: int, minutes_offset: int) -> 'DateTimeZone':
        """
        Returns a fixed offset zone based on hours and minutes.
        The sign of the hours and minutes must match, unless the total is zero.
        For example, (-2, -15) is valid, but (-2, 15) is not.
        """
        if hours_offset > 23 or hours_offset < -23:
            raise ValueError("Hours out of range: " + str(hours_offset))
        if minutes_offset > 59 or minutes_offset < -59:
            raise ValueError("Minutes out of range: " + str(minutes_offset))
        if hours_offset == 0 and minutes_offset == 0:
            return cls.UTC
        if (hours_offset > 0 and minutes_offset < 0) or (hours_offset < 0 and minutes_offset > 0):
            raise ValueError("Hours and minutes must have the same sign")
        total_minutes = hours_offset * 60 + minutes_offset
        if total_minutes > 23 * 60 + 59 or total_minutes < -23 * 60 - 59:
            raise ValueError("Total offset out of range: " + str(total_minutes))
        return cls.for_offset_millis(total_minutes * 60 * 1000)
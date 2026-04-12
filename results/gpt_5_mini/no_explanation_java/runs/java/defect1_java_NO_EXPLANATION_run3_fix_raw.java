public static DateTimeZone forOffsetHoursMinutes(int hoursOffset, int minutesOffset) throws IllegalArgumentException {
    if (hoursOffset == 0 && minutesOffset == 0) {
        return DateTimeZone.UTC;
    }
    if (hoursOffset < -23 || hoursOffset > 23) {
        throw new IllegalArgumentException("Hours out of range: " + hoursOffset);
    }
    if (minutesOffset < -59 || minutesOffset > 59) {
        throw new IllegalArgumentException("Minutes out of range: " + minutesOffset);
    }
    // Disallow combinations like (positive hours, negative minutes)
    if (hoursOffset > 0 && minutesOffset < 0) {
        throw new IllegalArgumentException("Positive hours must not have negative minutes: " + minutesOffset);
    }
    if (hoursOffset < 0 && minutesOffset > 0) {
        // Convert to negative total minutes (e.g. -2 hours and +15 minutes -> -135 minutes)
        // This is allowed.
    }
    int totalMinutes;
    try {
        if (hoursOffset < 0) {
            totalMinutes = hoursOffset * 60 - Math.abs(minutesOffset);
        } else {
            totalMinutes = hoursOffset * 60 + minutesOffset;
        }
        int offset = FieldUtils.safeMultiply(totalMinutes, DateTimeConstants.MILLIS_PER_MINUTE);
        return forOffsetMillis(offset);
    } catch (ArithmeticException ex) {
        throw new IllegalArgumentException("Offset is too large");
    }
}
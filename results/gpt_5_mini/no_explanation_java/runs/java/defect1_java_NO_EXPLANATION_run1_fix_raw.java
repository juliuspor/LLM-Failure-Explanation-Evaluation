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
    // Disallow positive hours with negative minutes
    if (hoursOffset > 0 && minutesOffset < 0) {
        throw new IllegalArgumentException("Positive hours must not have negative minutes: " + minutesOffset);
    }
    // Disallow negative hours with positive minutes? allowed (-2,15) -> -02:15 is allowed per docs, so allow.
    int totalMinutes;
    try {
        if (hoursOffset < 0) {
            // For negative hours, minutesOffset may be negative or positive; combine accordingly.
            totalMinutes = FieldUtils.safeAdd(FieldUtils.safeMultiply(hoursOffset, 60), minutesOffset);
        } else {
            totalMinutes = FieldUtils.safeAdd(FieldUtils.safeMultiply(hoursOffset, 60), minutesOffset);
        }
        int offset = FieldUtils.safeMultiply(totalMinutes, DateTimeConstants.MILLIS_PER_MINUTE);
        if (offset == 0) {
            return DateTimeZone.UTC;
        }
        return forOffsetMillis(offset);
    } catch (ArithmeticException ex) {
        throw new IllegalArgumentException("Offset is too large");
    }
}
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
    // disallow positive hours with negative minutes
    if (hoursOffset > 0 && minutesOffset < 0) {
        throw new IllegalArgumentException("Minutes must be positive when hours is positive");
    }
    // disallow negative hours with positive minutes? Actually allowed: (-2,15) -> -02:15 (negative hour and positive minutes allowed)
    // Determine total minutes
    int totalMinutes;
    if (hoursOffset > 0) {
        totalMinutes = hoursOffset * 60 + minutesOffset;
    } else if (hoursOffset < 0) {
        // if hours negative, minutesOffset may be negative or positive: both result in negative total
        totalMinutes = hoursOffset * 60 - Math.abs(minutesOffset);
    } else { // hoursOffset == 0
        totalMinutes = minutesOffset;
    }
    // Validate resulting totalMinutes within range +/- (23*60 + 59)
    int maxMinutes = 23 * 60 + 59;
    if (totalMinutes < -maxMinutes || totalMinutes > maxMinutes) {
        throw new IllegalArgumentException("Offset is too large");
    }
    int offset;
    try {
        offset = FieldUtils.safeMultiply(totalMinutes, DateTimeConstants.MILLIS_PER_MINUTE);
    } catch (ArithmeticException ex) {
        throw new IllegalArgumentException("Offset is too large");
    }
    return forOffsetMillis(offset);
}
public static String abbreviate(String str, int lower, int upper, String appendToEnd) {
    if (str == null) {
        return null;
    }
    if (str.length() == 0) {
        return StringUtils.EMPTY;
    }
    if (lower < 0) {
        lower = 0;
    }
    if (upper == -1 || upper > str.length()) {
        upper = str.length();
    }
    if (upper < lower) {
        upper = lower;
    }
    if (lower >= str.length()) {
        // nothing to abbreviate
        return str;
    }

    StringBuffer result = new StringBuffer();
    int index = StringUtils.indexOf(str, ' ', lower);
    if (index == -1) {
        // no space found after lower
        result.append(str.substring(0, upper));
        if (upper != str.length()) {
            result.append(StringUtils.defaultString(appendToEnd));
        }
    } else if (index > upper) {
        // first space after lower occurs beyond upper
        result.append(str.substring(0, upper));
        result.append(StringUtils.defaultString(appendToEnd));
    } else {
        // space found between lower and upper
        result.append(str.substring(0, index));
        result.append(StringUtils.defaultString(appendToEnd));
    }
    return result.toString();
}
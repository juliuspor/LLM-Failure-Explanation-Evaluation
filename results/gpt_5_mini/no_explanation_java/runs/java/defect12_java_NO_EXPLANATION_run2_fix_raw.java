public static String abbreviate(String str, int lower, int upper, String appendToEnd) {
    if (str == null) {
        return null;
    }
    if (str.length() == 0) {
        return org.apache.commons.lang.StringUtils.EMPTY;
    }

    if (upper == -1 || upper > str.length()) {
        upper = str.length();
    }
    if (upper < lower) {
        upper = lower;
    }

    // if the string is short enough, return it
    if (str.length() <= upper) {
        return str;
    }

    StringBuffer result = new StringBuffer();

    // find the last space between lower and upper
    int spaceIndex = str.lastIndexOf(' ', upper);
    if (spaceIndex < lower) {
        // no suitable space found; force-cut at upper
        result.append(str.substring(0, upper));
        // only append the appendToEnd if we actually abbreviated
        if (upper < str.length()) {
            result.append(org.apache.commons.lang.StringUtils.defaultString(appendToEnd));
        }
    } else {
        // break at the space found
        result.append(str.substring(0, spaceIndex));
        result.append(org.apache.commons.lang.StringUtils.defaultString(appendToEnd));
    }

    return result.toString();
}
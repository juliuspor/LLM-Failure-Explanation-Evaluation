public static Locale toLocale(String str) {
    if (str == null) {
        return null;
    }
    int len = str.length();
    if (len == 0) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    // language only: "en"
    if (len == 2) {
        char ch0 = str.charAt(0);
        char ch1 = str.charAt(1);
        if ((ch0 < 'a' || ch0 > 'z') || (ch1 < 'a' || ch1 > 'z')) {
            throw new IllegalArgumentException("Invalid locale format: " + str);
        }
        return new Locale(str, "");
    }
    // must have at least language + '_' + country (5) or language + '_' + country + '_' + variant (>=7)
    if (len < 5) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    // underscore after language
    if (str.charAt(2) != '_') {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    // country must be two letters
    if (len < 5) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    char ch3 = str.charAt(3);
    char ch4 = str.charAt(4);
    if ((ch3 < 'A' || ch3 > 'Z') || (ch4 < 'A' || ch4 > 'Z')) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    if (len == 5) {
        return new Locale(str.substring(0, 2), str.substring(3, 5));
    }
    // variant case: must have '_' at position 5 and variant non-empty
    if (str.charAt(5) != '_') {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    String variant = str.substring(6);
    if (variant.length() == 0) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    return new Locale(str.substring(0, 2), str.substring(3, 5), variant);
}
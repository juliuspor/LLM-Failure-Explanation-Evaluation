public static Locale toLocale(String str) {
    if (str == null) {
        return null;
    }
    int len = str.length();
    // valid lengths: 2 (language), 5 (language_country), or >=7 (language_country_variant)
    if (!(len == 2 || len == 5 || len >= 7)) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    // language: must be two lowercase letters
    if (len >= 2) {
        char ch0 = str.charAt(0);
        char ch1 = str.charAt(1);
        if (ch0 < 'a' || ch0 > 'z' || ch1 < 'a' || ch1 > 'z') {
            throw new IllegalArgumentException("Invalid locale format: " + str);
        }
    }
    if (len == 2) {
        return new Locale(str, "");
    }
    // from here, must have underscore at pos 2 and country two uppercase letters at 3-4
    if (str.charAt(2) != '_') {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    if (len < 5) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    char ch3 = str.charAt(3);
    char ch4 = str.charAt(4);
    if (ch3 < 'A' || ch3 > 'Z' || ch4 < 'A' || ch4 > 'Z') {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    if (len == 5) {
        return new Locale(str.substring(0, 2), str.substring(3, 5));
    }
    // variant case: must have underscore at pos 5 and non-empty variant after
    if (str.charAt(5) != '_') {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    String variant = str.substring(6);
    return new Locale(str.substring(0, 2), str.substring(3, 5), variant);
}
public static Locale toLocale(String str) {
    if (str == null) {
        return null;
    }
    int len = str.length();
    // Valid lengths: 2 (language), 5 (language_country), or >=7 (language_country_variant)
    if (!(len == 2 || len == 5 || len >= 7)) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    // language must be two lowercase letters
    if (len < 2) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    char ch0 = str.charAt(0);
    char ch1 = str.charAt(1);
    if (ch0 < 'a' || ch0 > 'z' || ch1 < 'a' || ch1 > 'z') {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    if (len == 2) {
        return new Locale(str, "");
    }
    // For len >= 5, position 2 must be '_'
    if (str.charAt(2) != '_') {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    if (len == 5) {
        // country must be two uppercase letters
        char ch3 = str.charAt(3);
        char ch4 = str.charAt(4);
        if (ch3 < 'A' || ch3 > 'Z' || ch4 < 'A' || ch4 > 'Z') {
            throw new IllegalArgumentException("Invalid locale format: " + str);
        }
        return new Locale(str.substring(0, 2), str.substring(3, 5));
    }
    // len >= 7 -> must have '_' at position 5 and variant of length >=1
    if (str.charAt(5) != '_') {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    // validate country
    char ch3 = str.charAt(3);
    char ch4 = str.charAt(4);
    if (ch3 < 'A' || ch3 > 'Z' || ch4 < 'A' || ch4 > 'Z') {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    // variant may be any non-empty string
    String variant = str.substring(6);
    if (variant.length() == 0) {
        throw new IllegalArgumentException("Invalid locale format: " + str);
    }
    return new Locale(str.substring(0, 2), str.substring(3, 5), variant);
}
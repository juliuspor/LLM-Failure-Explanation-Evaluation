    /**
     * Abbreviates a string nicely.
     * 
     * This method searches for the first space after the lower limit and abbreviates
     * the String there. It will also append any String passed as a parameter
     * to the end of the String. The upper limit can be specified to forcibly
     * abbreviate a String.
     * 
     * @param str         the string to be abbreviated. If null is passed, null is returned.
     *                    If the empty String is passed, the empty string is returned.
     * @param lower       the lower limit.
     * @param upper       the upper limit; specify -1 if no limit is desired.
     *                    If the upper limit is lower than the lower limit, it will be
     *                    adjusted to be the same as the lower limit.
     * @param appendToEnd String to be appended to the end of the abbreviated string.
     *                    This is appended ONLY if the string was indeed abbreviated.
     *                    The append does not count towards the lower or upper limits.
     * @return the abbreviated String.
     * @since 2.4
     */
    public static String abbreviate(String str, int lower, int upper, String appendToEnd) {
        // initial parameter checks
        if (str == null) {
            return null;
        }
        if (str.length() == 0) {
            return "";
        }

        // if the upper value is -1 (i.e. no limit) or is greater
        // than the length of the string, set to the length of the string
        if (upper == -1 || upper > str.length()) {
            upper = str.length();
        }
        // if upper is less than lower, raise it to lower
        if (upper < lower) {
            upper = lower;
        }

        StringBuffer result = new StringBuffer(str.length() + 8);
        
        // Find first space at or after lower, but before or at upper
        int index = -1;
        for (int i = lower; i <= upper && i < str.length(); i++) {
            if (str.charAt(i) == ' ') {
                index = i;
                break;
            }
        }
        
        String abbreviated;
        if (index != -1) {
            // Found space within limits
            abbreviated = str.substring(0, index);
        } else {
            // No space found, truncate at upper
            abbreviated = str.substring(0, upper);
        }
        
        // Only append if actual abbreviation occurred
        if (abbreviated.length() < str.length()) {
            result.append(abbreviated);
            if (appendToEnd != null) {
                result.append(appendToEnd);
            }
        } else {
            result.append(str);
        }
        
        return result.toString();
    }
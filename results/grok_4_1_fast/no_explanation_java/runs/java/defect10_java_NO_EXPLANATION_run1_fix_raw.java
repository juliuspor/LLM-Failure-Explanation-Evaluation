    /**
     * <p>Turns a string value into a java.lang.Number.</p>
     *
     * <p>First, the value is examined for a type qualifier on the end
     * (<code>'f','F','d','D','l','L'</code>).  If it is found, it starts 
     * trying to create successively larger types from the type specified
     * until one is found that can hold the value.</p>
     *
     * <p>If a type specifier is not found, it will check for a decimal point
     * and then try successively larger types from <code>Integer</code> to
     * <code>BigInteger</code> and from <code>Float</code> to
     * <code>BigDecimal</code>.</p>
     *
     * <p>If the string starts with <code>0x</code> or <code>-0x</code>, it
     * will be interpreted as a hexadecimal integer.  Values with leading
     * <code>0</code>'s will not be interpreted as octal.</p>
     *
     * @param val String containing a number
     * @return Number created from the string
     * @throws NumberFormatException if the value cannot be converted
     */
    public static Number createNumber(String val) throws NumberFormatException {
        if (val == null) {
            return null;
        }
        if (val.length() == 0) {
            throw new NumberFormatException("\"\" is not a valid number.");
        }
        if (val.startsWith("--")) {
            // this is protection for poorness in java.lang.BigDecimal.
            // it accepts this as a legal value, but it does not appear 
            // to be in specification of class. OS X Java parses it to 
            // a wrong value.
            return null;
        }
        if (val.startsWith("0x") || val.startsWith("-0x")) {
            return createInteger(val);
        }   
        
        char lastChar = val.charAt(val.length() - 1);
        boolean hasTypeSuffix = !Character.isDigit(lastChar);
        
        if (hasTypeSuffix) {
            String numeric = val.substring(0, val.length() - 1);
            boolean allZeros = isAllZeros(numeric);
            
            switch (Character.toLowerCase(lastChar)) {
                case 'l':
                    if (isValidIntegerString(numeric)) {
                        try {
                            return createLong(numeric);
                        } catch (NumberFormatException nfe) {
                            // Too big for long
                        }
                        return createBigInteger(numeric);
                    }
                    throw new NumberFormatException(val + " is not a valid number.");
                    
                case 'f':
                    try {
                        Float f = createFloat(numeric);
                        if (!f.isInfinite() && !(f.floatValue() == 0.0f && !allZeros)) {
                            return f;
                        }
                    } catch (NumberFormatException ignored) {}
                    // Fall through to double
                case 'd':
                    try {
                        Double d = createDouble(numeric);
                        if (!d.isInfinite() && !(d.doubleValue() == 0.0 && !allZeros)) {
                            return d;
                        }
                    } catch (NumberFormatException ignored) {}
                    return createBigDecimal(numeric);
                    
                default:
                    throw new NumberFormatException(val + " is not a valid number.");
            }
        } else {
            // No type suffix - try integer types first, then floating point
            if (val.indexOf('.') == -1 && val.toLowerCase().indexOf('e') == -1) {
                // No decimal or exponent - must be integer
                try {
                    return createInteger(val);
                } catch (NumberFormatException ignored) {}
                try {
                    return createLong(val);
                } catch (NumberFormatException ignored) {}
                return createBigInteger(val);
            } else {
                // Has decimal or exponent - must be floating point
                boolean allZeros = isAllZeros(val);
                try {
                    Float f = createFloat(val);
                    if (!f.isInfinite() && !(f.floatValue() == 0.0f && !allZeros)) {
                        return f;
                    }
                } catch (NumberFormatException ignored) {}
                try {
                    Double d = createDouble(val);
                    if (!d.isInfinite() && !(d.doubleValue() == 0.0 && !allZeros)) {
                        return d;
                    }
                } catch (NumberFormatException ignored) {}
                return createBigDecimal(val);
            }
        }
    }

    private static boolean isValidIntegerString(String str) {
        if (str == null || str.isEmpty()) return false;
        boolean negative = str.charAt(0) == '-';
        String digits = negative ? str.substring(1) : str;
        return isDigits(digits);
    }
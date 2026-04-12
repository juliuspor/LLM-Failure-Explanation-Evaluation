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
        int decPos = val.indexOf('.');
        int expPos = Math.max(val.indexOf('e'), val.indexOf('E'));
        
        if (!Character.isDigit(lastChar)) {
            // Requesting a specific type
            String numeric = val.substring(0, val.length() - 1);
            boolean allZeros = isAllZeros(val.substring(0, val.length() - 1));
            
            switch (lastChar) {
                case 'l':
                case 'L':
                    if (decPos == -1 && expPos == -1 && 
                        (numeric.charAt(0) == '-' && isDigits(numeric.substring(1)) || isDigits(numeric))) {
                        try {
                            return createLong(numeric);
                        } catch (NumberFormatException nfe) {
                            // Too big for a long
                        }
                        return createBigInteger(numeric);
                    }
                    throw new NumberFormatException(val + " is not a valid number.");
                    
                case 'f':
                case 'F':
                    try {
                        Float f = createFloat(numeric);
                        if (!(f.isInfinite() || (f.floatValue() == 0.0f && !allZeros))) {
                            return f;
                        }
                    } catch (NumberFormatException e) {
                        // ignore the bad number
                    }
                    // Fall through
                case 'd':
                case 'D':
                    try {
                        Double d = createDouble(numeric);
                        if (!(d.isInfinite() || (d.doubleValue() == 0.0 && !allZeros))) {
                            return d;
                        }
                    } catch (NumberFormatException nfe) {
                        // ignore
                    }
                    return createBigDecimal(numeric);
                    
                default:
                    throw new NumberFormatException(val + " is not a valid number.");
            }
        } else {
            // No type specifier, choose based on content
            if (decPos > -1 || expPos > -1) {
                // Decimal or scientific notation
                boolean allZeros = isAllZeros(val);
                try {
                    Float f = createFloat(val);
                    if (!(f.isInfinite() || (f.floatValue() == 0.0f && !allZeros))) {
                        return f;
                    }
                } catch (NumberFormatException nfe) {
                    // ignore
                }
                try {
                    Double d = createDouble(val);
                    if (!(d.isInfinite() || (d.doubleValue() == 0.0 && !allZeros))) {
                        return d;
                    }
                } catch (NumberFormatException nfe) {
                    // ignore
                }
                return createBigDecimal(val);
            } else {
                // Integral number
                try {
                    return createInteger(val);
                } catch (NumberFormatException nfe) {
                    // ignore
                }
                try {
                    return createLong(val);
                } catch (NumberFormatException nfe) {
                    // ignore
                }
                return createBigInteger(val);
            }
        }
    }
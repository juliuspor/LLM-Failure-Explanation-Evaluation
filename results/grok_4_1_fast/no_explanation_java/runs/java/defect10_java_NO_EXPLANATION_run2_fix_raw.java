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
        boolean hasTypeQualifier = !Character.isDigit(lastChar);
        
        // Find decimal and exponent positions
        int decPos = val.indexOf('.');
        int expPos = -1;
        int ePos = val.indexOf('e');
        int ePos2 = val.indexOf('E');
        if (ePos == -1) {
            expPos = ePos2;
        } else if (ePos2 == -1 || ePos < ePos2) {
            expPos = ePos;
        } else {
            expPos = ePos2;
        }
        expPos++;
        
        if (!hasTypeQualifier) {
            // No type qualifier - try integer types first, then floating point
            if (decPos == -1 && expPos == -1) {
                // Must be an int, long, bigint
                try {
                    return createInteger(val);
                } catch (NumberFormatException nfe) {
                    // empty catch
                }
                try {
                    return createLong(val);
                } catch (NumberFormatException nfe) {
                    // empty catch
                }
                return createBigInteger(val);
            } else {
                // Must be float, double, BigDecimal
                boolean allZeros = isAllZeros(decPos == -1 ? "" : val.substring(decPos + 1)) && 
                                 (expPos == -1 ? true : isAllZeros(val.substring(expPos)));
                try {
                    Float f = createFloat(val);
                    if (!(f.isInfinite() || (f.floatValue() == 0.0F && !allZeros))) {
                        return f;
                    }
                } catch (NumberFormatException nfe) {
                    // empty catch
                }
                try {
                    Double d = createDouble(val);
                    if (!(d.isInfinite() || (d.doubleValue() == 0.0D && !allZeros))) {
                        return d;
                    }
                } catch (NumberFormatException nfe) {
                    // empty catch
                }
                return createBigDecimal(val);
            }
        } else {
            // Has type qualifier
            String numeric = val.substring(0, val.length() - 1);
            boolean allZeros = isAllZeros(decPos == -1 ? "" : val.substring(decPos + 1, val.length() - 1)) && 
                             (expPos == -1 || expPos >= val.length() - 1 || isAllZeros(val.substring(expPos, val.length() - 1)));
            
            switch (lastChar) {
                case 'l' :
                case 'L' :
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
                    
                case 'f' :
                case 'F' :
                    try {
                        Float f = NumberUtils.createFloat(numeric);
                        if (!(f.isInfinite() || (f.floatValue() == 0.0F && !allZeros))) {
                            return f;
                        }
                    } catch (NumberFormatException e) {
                        // ignore the bad number
                    }
                    // Fall through
                case 'd' :
                case 'D' :
                    try {
                        Double d = NumberUtils.createDouble(numeric);
                        if (!(d.isInfinite() || (d.doubleValue() == 0.0D && !allZeros))) {
                            return d;
                        }
                    } catch (NumberFormatException nfe) {
                        // empty catch
                    }
                    try {
                        return createBigDecimal(numeric);
                    } catch (NumberFormatException e) {
                        // empty catch
                    }
                    throw new NumberFormatException(val + " is not a valid number.");
                    
                default :
                    throw new NumberFormatException(val + " is not a valid number.");
            }
        }
    }
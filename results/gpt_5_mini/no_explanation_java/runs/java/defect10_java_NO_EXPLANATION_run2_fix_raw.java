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
        String trimmed = val;
        // handle optional leading + for hex as well
        if (trimmed.startsWith("0x") || trimmed.startsWith("-0x") || trimmed.startsWith("+0x")) {
            return createInteger(trimmed);
        }
        char lastChar = trimmed.charAt(trimmed.length() - 1);
        String mant;
        String dec;
        String exp;
        int decPos = trimmed.indexOf('.');
        int expPos = trimmed.indexOf('e');
        if (expPos == -1) {
            expPos = trimmed.indexOf('E');
        }

        if (decPos > -1) {

            if (expPos > -1) {
                if (expPos < decPos) {
                    throw new NumberFormatException(trimmed + " is not a valid number.");
                }
                dec = trimmed.substring(decPos + 1, expPos);
            } else {
                dec = trimmed.substring(decPos + 1);
            }
            mant = trimmed.substring(0, decPos);
        } else {
            if (expPos > -1) {
                mant = trimmed.substring(0, expPos);
            } else {
                mant = trimmed;
            }
            dec = null;
        }
        if (!Character.isDigit(lastChar)) {
            if (expPos > -1 && expPos < trimmed.length() - 1) {
                exp = trimmed.substring(expPos + 1, trimmed.length() - 1);
            } else {
                exp = null;
            }
            //Requesting a specific type..
            String numeric = trimmed.substring(0, trimmed.length() - 1);
            boolean allZeros = isAllZeros(mant) && isAllZeros(exp);
            switch (lastChar) {
                case 'l' :
                case 'L' :
                    if (dec == null
                        && exp == null
                        && (numeric.charAt(0) == '-' && isDigits(numeric.substring(1)) || isDigits(numeric))) {
                        try {
                            return createLong(numeric);
                        } catch (NumberFormatException nfe) {
                            //Too big for a long
                        }
                        return createBigInteger(numeric);

                    }
                    throw new NumberFormatException(trimmed + " is not a valid number.");
                case 'f' :
                case 'F' :
                    try {
                        Float f = NumberUtils.createFloat(numeric);
                        if (!(f.isInfinite() || (f.floatValue() == 0.0F && !allZeros))) {
                            //If it's too big for a float or the float value = 0 and the string
                            //has non-zeros in it, then float does not have the precision we want
                            return f;
                        }

                    } catch (NumberFormatException e) {
                        // ignore the bad number
                    }
                    //Fall through
                case 'd' :
                case 'D' :
                    try {
                        Double d = NumberUtils.createDouble(numeric);
                        if (!(d.isInfinite() || (d.floatValue() == 0.0D && !allZeros))) {
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
                    //Fall through
                default :
                    throw new NumberFormatException(trimmed + " is not a valid number.");

            }
        } else {
            //User doesn't have a preference on the return type, so let's start
            //small and go from there...
            if (expPos > -1 && expPos < trimmed.length() - 1) {
                exp = trimmed.substring(expPos + 1, trimmed.length());
            } else {
                exp = null;
            }
            if (dec == null && exp == null) {
                //Must be an int,long,bigint
                try {
                    return createInteger(trimmed);
                } catch (NumberFormatException nfe) {
                    // empty catch
                }
                try {
                    return createLong(trimmed);
                } catch (NumberFormatException nfe) {
                    // empty catch
                }
                return createBigInteger(trimmed);

            } else {
                //Must be a float,double,BigDec
                boolean allZeros = isAllZeros(mant) && isAllZeros(exp);
                try {
                    Float f = createFloat(trimmed);
                    if (!(f.isInfinite() || (f.floatValue() == 0.0F && !allZeros))) {
                        return f;
                    }
                } catch (NumberFormatException nfe) {
                    // empty catch
                }
                try {
                    Double d = createDouble(trimmed);
                    if (!(d.isInfinite() || (d.doubleValue() == 0.0D && !allZeros))) {
                        return d;
                    }
                } catch (NumberFormatException nfe) {
                    // empty catch
                }

                return createBigDecimal(trimmed);

            }

        }
    }
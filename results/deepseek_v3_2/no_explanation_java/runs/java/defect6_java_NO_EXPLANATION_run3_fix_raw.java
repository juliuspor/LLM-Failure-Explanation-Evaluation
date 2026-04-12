  void addNumber(double x) {
    // This is not pretty printing. This is to prevent misparsing of x- -4 as
    // x--4 (which is a syntax error).
    char prev = getLastChar();
    if (x < 0 && prev == '-') {
      add(" ");
    }

    if (x == Double.POSITIVE_INFINITY) {
      add("Infinity");
    } else if (x == Double.NEGATIVE_INFINITY) {
      add("-Infinity");
    } else if (Double.isNaN(x)) {
      add("NaN");
    } else if (isNegativeZero(x)) {
      // Negative zero must be printed as "-0" to preserve the sign.
      add("-0");
    } else if ((long) x == x) {
      long value = (long) x;
      long absValue = Math.abs(value);
      if (absValue >= 100) {
        // Try to represent as mantissa * 10^exp where 1 <= mantissa < 10
        int exp = 0;
        long mantissa = absValue;
        while (mantissa >= 10 && mantissa % 10 == 0) {
          mantissa /= 10;
          exp++;
        }
        if (exp > 2) {
          // Use scientific notation
          String sign = value < 0 ? "-" : "";
          add(sign + Long.toString(mantissa) + "E" + Integer.toString(exp));
          return;
        }
      }
      // Plain integer representation
      add(Long.toString(value));
    } else {
      // For non-integer doubles, use default string representation.
      // Ensure it doesn't use scientific notation for small numbers.
      add(String.valueOf(x));
    }
  }
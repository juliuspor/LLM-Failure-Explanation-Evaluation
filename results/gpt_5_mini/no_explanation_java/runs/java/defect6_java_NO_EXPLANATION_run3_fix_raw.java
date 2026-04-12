void addNumber(double x) {
    // Prevent misparsing of x- -4 as x--4
    char prev = getLastChar();
    if (x < 0 && prev == '-') {
      add(" ");
    }

    if (isNegativeZero(x)) {
      // Java prints -0.0; preserve sign
      add("-0");
      return;
    }

    // Check if x is an integer value that fits in a long
    if (x == Math.rint(x)) {
      double dx = x;
      // Check range for long
      if (dx <= Long.MAX_VALUE && dx >= Long.MIN_VALUE) {
        long value = (long) dx;
        long absVal = Math.abs(value);
        int exp = 0;
        // Strip trailing zeros for large numbers to produce mantissa and exponent
        if (absVal >= 100) {
          while (absVal % 10 == 0) {
            absVal /= 10;
            exp++;
          }
        }
        if (exp > 2) {
          String mantissa = (value < 0 ? "-" : "") + Long.toString(absVal);
          add(mantissa + "E" + Integer.toString(exp));
        } else {
          add(Long.toString(value));
        }
        return;
      }
    }

    // Fallback for non-integer or out-of-range values
    add(String.valueOf(x));
  }
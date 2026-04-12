void addNumber(double x) {
    // Prevent misparsing of x- -4 as x--4
    char prev = getLastChar();
    if (x < 0 && prev == '-') {
      add(" ");
    }

    // Handle negative zero explicitly
    if (isNegativeZero(x)) {
      add("-0");
      return;
    }

    // If x is an integer value and within long range, format without decimal
    if (x == Math.rint(x) && x >= Long.MIN_VALUE && x <= Long.MAX_VALUE) {
      long value = (long) x;
      long absVal = Math.abs(value);
      int exp = 0;
      long mantissa = absVal;

      // Reduce by factors of 10 to get mantissa and exponent
      while (mantissa >= 10 && mantissa % 10 == 0) {
        mantissa /= 10;
        exp++;
      }

      String out;
      if (exp > 2) {
        // Preserve sign
        out = (value < 0 ? "-" : "") + Long.toString(mantissa) + "E" + Integer.toString(exp);
      } else {
        out = Long.toString(value);
      }
      add(out);
    } else {
      // Non-integer or out of long range: use default string conversion
      add(Double.toString(x));
    }
  }
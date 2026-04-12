void addNumber(double x) {
    // Prevent misparsing of x- -4 as x--4 (which is a syntax error).
    char prev = getLastChar();
    if (x < 0 && prev == '-') {
      add(" ");
    }

    // Handle negative zero explicitly.
    if (isNegativeZero(x)) {
      add("-0");
      return;
    }

    // If x is a mathematical integer and fits in a long, print as integer.
    if (Math.floor(x) == x && Math.abs(x) <= Long.MAX_VALUE) {
      long value = (long) x;

      long mantissa = value;
      int exp = 0;

      // Remove trailing zeros to possibly use exponential form like 1E3
      if (Math.abs(value) >= 100) {
        while (mantissa % 10 == 0 && mantissa != 0) {
          mantissa /= 10;
          exp++;
        }
      }

      if (exp > 2) {
        add(Long.toString(mantissa) + "E" + Integer.toString(exp));
      } else {
        add(Long.toString(value));
      }
    } else {
      // Otherwise, use standard double representation.
      add(String.valueOf(x));
    }
  }
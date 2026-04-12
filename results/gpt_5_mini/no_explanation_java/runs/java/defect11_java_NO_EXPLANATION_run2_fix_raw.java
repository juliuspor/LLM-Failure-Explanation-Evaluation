public static String random(int count, int start, int end, boolean letters, boolean numbers,
                                char[] chars, Random random) {
        if (count == 0) {
            return "";
        } else if (count < 0) {
            throw new IllegalArgumentException("Requested random string length " + count + " is less than 0.");
        }
        if (chars != null && chars.length == 0) {
            throw new IllegalArgumentException("The chars array must not be empty");
        }

        if (start == 0 && end == 0) {
            if (chars != null) {
                end = chars.length;
            } else {
                if (!letters && !numbers) {
                    end = Integer.MAX_VALUE;
                } else {
                    end = 'z' + 1;
                    start = ' ';
                }
            }
        }

        char[] buffer = new char[count];
        int gap = end - start;
        if (chars == null && gap <= 0) {
            throw new IllegalArgumentException("Invalid start and end range: " + start + " to " + end);
        }
        if (chars != null && gap <= 0) {
            throw new ArrayIndexOutOfBoundsException("Error: End value must be greater than start when chars array is provided");
        }

        int pos = 0;
        while (pos < count) {
            char ch;
            if (chars == null) {
                // when end might be Integer.MAX_VALUE, random.nextInt(gap) may overflow; but gap is int, and random.nextInt requires positive int
                ch = (char) (random.nextInt(gap) + start);
            } else {
                ch = chars[random.nextInt(gap) + start];
            }

            if (letters && Character.isLetter(ch)
                    || numbers && Character.isDigit(ch)
                    || !letters && !numbers) {
                // handle low surrogate
                if (ch >= 56320 && ch <= 57343) {
                    // low surrogate should be placed after a high surrogate; if no room left, skip
                    if (pos + 1 > count - 1) {
                        continue; // no room for pair
                    }
                    // insert high then low
                    buffer[pos++] = (char) (55296 + random.nextInt(128));
                    buffer[pos++] = ch;
                } else if (ch >= 55296 && ch <= 56191) {
                    // high surrogate should be followed by low surrogate
                    if (pos + 1 > count - 1) {
                        continue; // no room for pair
                    }
                    buffer[pos++] = ch;
                    buffer[pos++] = (char) (56320 + random.nextInt(128));
                } else if (ch >= 56192 && ch <= 56319) {
                    // private high surrogate, skip
                    continue;
                } else {
                    buffer[pos++] = ch;
                }
            } else {
                // char did not match letter/number constraints, try again
                continue;
            }
        }
        return new String(buffer);
    }
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

    int pos = 0; // position in buffer to fill
    while (pos < count) {
        char ch;
        if (chars == null) {
            if (gap <= 0) {
                // when using full char range and letters/numbers false, use random int cast to char
                ch = (char) random.nextInt();
            } else {
                ch = (char) (random.nextInt(gap) + start);
            }
        } else {
            // when chars provided, gap should be chars.length and start should be 0..length-1
            if (gap <= 0) {
                throw new IllegalArgumentException("Start and end invalid for chars array");
            }
            ch = chars[random.nextInt(gap) + start];
        }

        if (letters && Character.isLetter(ch)
                || numbers && Character.isDigit(ch)
                || !letters && !numbers) {
            // handle low surrogate
            if (ch >= 0xDC00 && ch <= 0xDFFF) { // 56320 to 57343
                // low surrogate - need a high surrogate before it
                if (pos + 1 > count - 1) {
                    // not enough space to insert pair, skip
                    continue;
                }
                buffer[pos++] = (char) (0xD800 + random.nextInt(0x80)); // high surrogate 0xD800..0xDB7F
                buffer[pos++] = ch;
            } else if (ch >= 0xD800 && ch <= 0xDB7F) { // 55296 to 56191 high surrogate
                // high surrogate - need a low surrogate after it
                if (pos + 1 > count - 1) {
                    // not enough space, skip
                    continue;
                }
                buffer[pos++] = ch;
                buffer[pos++] = (char) (0xDC00 + random.nextInt(0x80)); // low surrogate 0xDC00..0xDFFF
            } else if (ch >= 0xDB80 && ch <= 0xDBFF) { // 56192 to 56319 private high surrogate - skip
                continue;
            } else {
                buffer[pos++] = ch;
            }
        } else {
            // character did not match criteria, try again
            continue;
        }
    }
    return new String(buffer);
}
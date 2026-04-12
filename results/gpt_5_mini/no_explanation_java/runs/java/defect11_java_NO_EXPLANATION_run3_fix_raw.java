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

        int written = 0;
        while (written < count) {
            char ch;
            if (chars == null) {
                ch = (char) (random.nextInt(gap) + start);
            } else {
                ch = chars[random.nextInt(gap) + start];
            }
            if (letters && Character.isLetter(ch)
                    || numbers && Character.isDigit(ch)
                    || !letters && !numbers) {
                // handle low surrogate
                if (ch >= 0xDC00 && ch <= 0xDFFF) { // 56320 to 57343
                    if (written + 1 >= count) {
                        // not enough room for surrogate pair, skip
                        continue;
                    }
                    buffer[written++] = ch;
                    buffer[written++] = (char) (0xD800 + random.nextInt(0x80)); // 55296 + 128
                } else if (ch >= 0xD800 && ch <= 0xDB7F) { // 55296 to 56191
                    if (written + 1 >= count) {
                        // not enough room for surrogate pair, skip
                        continue;
                    }
                    buffer[written++] = (char) (0xDC00 + random.nextInt(0x80)); // 56320 + 128
                    buffer[written++] = ch;
                } else if (ch >= 0xDB80 && ch <= 0xDBFF) { // 56192 to 56319 private high surrogate - skip
                    continue;
                } else {
                    buffer[written++] = ch;
                }
            } else {
                // doesn't match letter/number constraints, skip
                continue;
            }
        }
        return new String(buffer);
    }
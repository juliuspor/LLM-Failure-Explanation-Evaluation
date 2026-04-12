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

        int gap = end - start;
        if (gap <= 0) {
            throw new IllegalArgumentException("Invalid range: end - start + 1 must be positive (end=" + end + ", start=" + start + ")");
        }

        char[] buffer = new char[count];
        int idx = 0;

        while (idx < count) {
            char ch;
            if (chars == null) {
                ch = (char) (random.nextInt(gap) + start);
            } else {
                ch = chars[random.nextInt(gap) + start];
            }
            if (letters && Character.isLetter(ch)
                    || numbers && Character.isDigit(ch)
                    || !letters && !numbers) {
                if(ch >= 56320 && ch <= 57343) {
                    // low surrogate, insert high surrogate before it
                    if (idx + 1 < count) {
                        buffer[idx] = (char) (55296 + random.nextInt(128));
                        buffer[idx + 1] = ch;
                        idx += 2;
                    } else {
                        // not enough space for pair, skip
                        idx++;
                    }
                } else if(ch >= 55296 && ch <= 56191) {
                    // high surrogate, insert low surrogate after it
                    if (idx + 1 < count) {
                        buffer[idx] = ch;
                        buffer[idx + 1] = (char) (56320 + random.nextInt(128));
                        idx += 2;
                    } else {
                        // not enough space for pair, skip
                        idx++;
                    }
                } else if(ch >= 56192 && ch <= 56319) {
                    // private high surrogate, skip it
                    idx++;
                } else {
                    buffer[idx] = ch;
                    idx++;
                }
            } else {
                idx++;
            }
        }
        return new String(buffer);
    }
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

        if (gap <= 0) {
            throw new IllegalArgumentException("Parameter gap (" + gap + ") must be positive.");
        }

        int index = 0;
        while (index < count) {
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
                    if(index == count - 1) {
                        // low surrogate, need space for high surrogate, so skip and retry
                        continue;
                    } else {
                        // low surrogate, insert high surrogate after putting it in
                        buffer[index] = ch;
                        index++;
                        buffer[index] = (char) (55296 + random.nextInt(128));
                    }
                } else if(ch >= 55296 && ch <= 56191) {
                    if(index == count - 1) {
                        // high surrogate, need space for low surrogate, so skip and retry
                        continue;
                    } else {
                        // high surrogate, insert low surrogate before putting it in
                        buffer[index] = (char) (56320 + random.nextInt(128));
                        index++;
                        buffer[index] = ch;
                    }
                } else if(ch >= 56192 && ch <= 56319) {
                    // private high surrogate, skip it
                    continue;
                } else {
                    buffer[index] = ch;
                }
                index++;
            } else {
                // character not allowed, retry
                continue;
            }
        }
        return new String(buffer);
    }
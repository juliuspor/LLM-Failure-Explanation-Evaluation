private static String replaceEach(String text, String[] searchList, String[] replacementList, 
                                      boolean repeat, int timeToLive) 
    {

        if (text == null || text.length() == 0 || searchList == null || 
            searchList.length == 0 || replacementList == null || replacementList.length == 0) 
        {
            return text;
        }

        if (timeToLive < 0) {
            throw new IllegalStateException("TimeToLive of " + timeToLive + " is less than 0: " + text);
        }

        int searchLength = searchList.length;
        int replacementLength = replacementList.length;

        if (searchLength != replacementLength) {
            throw new IllegalArgumentException("Search and Replace array lengths don't match: "
                + searchLength
                + " vs "
                + replacementLength);
        }

        boolean[] noMoreMatchesForReplIndex = new boolean[searchLength];

        int textIndex = -1;
        int replaceIndex = -1;
        int tempIndex = -1;

        for (int i = 0; i < searchLength; i++) {
            if (noMoreMatchesForReplIndex[i] || searchList[i] == null || 
                searchList[i].length() == 0) 
            {
                continue;
            }
            if (replacementList[i] == null) {
                // treat null replacement as empty -> still a valid search but replacement is empty
            }
            tempIndex = text.indexOf(searchList[i]);

            if (tempIndex == -1) {
                noMoreMatchesForReplIndex[i] = true;
            } else {
                if (textIndex == -1 || tempIndex < textIndex) {
                    textIndex = tempIndex;
                    replaceIndex = i;
                }
            }
        }

        if (textIndex == -1) {
            return text;
        }

        int start = 0;

        int increase = 0;

        for (int i = 0; i < searchLength; i++) {
            String search = searchList[i];
            String replace = replacementList[i];
            if (search == null || replace == null) {
                if (search == null) {
                    continue;
                }
                // if replace is null treat as ""
                replace = EMPTY;
            }
            int greater = replace.length() - search.length();
            if (greater > 0) {
                increase += 3 * greater;
            }
        }

        increase = Math.min(increase, text.length() / 5);

        StringBuilder buf = new StringBuilder(text.length() + increase);

        while (textIndex != -1) {

            for (int i = start; i < textIndex; i++) {
                buf.append(text.charAt(i));
            }
            String repl = replacementList[replaceIndex];
            if (repl == null) {
                repl = EMPTY;
            }
            buf.append(repl);

            start = textIndex + searchList[replaceIndex].length();

            textIndex = -1;
            replaceIndex = -1;
            tempIndex = -1;

            for (int i = 0; i < searchLength; i++) {
                if (noMoreMatchesForReplIndex[i] || searchList[i] == null || 
                    searchList[i].length() == 0) 
                {
                    continue;
                }
                tempIndex = text.indexOf(searchList[i], start);

                if (tempIndex == -1) {
                    noMoreMatchesForReplIndex[i] = true;
                } else {
                    if (textIndex == -1 || tempIndex < textIndex) {
                        textIndex = tempIndex;
                        replaceIndex = i;
                    }
                }
            }

        }
        int textLength = text.length();
        for (int i = start; i < textLength; i++) {
            buf.append(text.charAt(i));
        }
        String result = buf.toString();
        if (!repeat) {
            return result;
        }

        return replaceEach(result, searchList, replacementList, repeat, timeToLive - 1);
    }
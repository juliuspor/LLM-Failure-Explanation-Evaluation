    @staticmethod
    def replace_each(
        text: Optional[str],
        search_list: Optional[List[Optional[str]]],
        replacement_list: Optional[List[Optional[str]]],
    ) -> Optional[str]:
        if text is None:
            return None
        if text == "":
            return ""
        if search_list is None or replacement_list is None:
            return text
        if len(search_list) == 0 or len(replacement_list) == 0:
            return text
        if len(search_list) != len(replacement_list):
            raise ValueError(
                f"Search and Replace array lengths don't match: {len(search_list)} vs {len(replacement_list)}"
            )

        # We'll work on a mutable list of characters (or just a string builder) but for simplicity, we can process sequentially.
        # The key is to apply replacements in order of appearance, but after each replacement, the string changes.
        # We'll use a while loop that scans from the current position, but we need to consider the updated string.
        # We'll keep a working string that we update as we go.
        working_text = text
        # We need to track the current position in the working_text, but we also need to find the earliest match among all search strings.
        # However, after a replacement, earlier positions may have changed, so we must restart scanning from the beginning of the working_text?
        # Actually, we can continue from the position after the replacement, but we must use the updated working_text.
        # The algorithm: while True:
        #   Find the earliest match among all search strings starting from current index.
        #   If no match, break.
        #   Perform replacement at that match.
        #   Update working_text and set current index to the position after the replacement.
        # However, we must also skip search strings that are empty or None, and replacements that are None.
        # We also need to avoid infinite loops if a replacement contains the search string (like typical replace).
        # The original algorithm intended to avoid re-checking already processed parts, but it used the original text.
        # We'll implement a new loop that uses the working_text.

        # Pre-process search and replacement pairs: filter out invalid ones.
        pairs = []
        for i in range(len(search_list)):
            search = search_list[i]
            replacement = replacement_list[i]
            if search is None or len(search) == 0 or replacement is None:
                # Skip this pair, as it won't be used.
                continue
            pairs.append((search, replacement))

        if not pairs:
            return working_text

        # We'll use a while loop that scans from the start of the working_text.
        # But we need to ensure we don't get stuck in an infinite loop if a replacement contains the search string.
        # The typical behavior of replace_each in Apache Commons Lang is to not re-scan the replaced part.
        # So we advance the start index after the replacement.
        start = 0
        # We'll build the result incrementally using a list of parts.
        parts = []
        # We need to find the earliest match among all pairs from start.
        while True:
            earliest_index = -1
            earliest_pair = None
            earliest_search_len = 0
            for search, replacement in pairs:
                # Find the first occurrence of search in working_text starting from start.
                index = working_text.find(search, start)
                if index != -1:
                    if earliest_index == -1 or index < earliest_index:
                        earliest_index = index
                        earliest_pair = (search, replacement)
                        earliest_search_len = len(search)
            if earliest_index == -1:
                # No more matches.
                parts.append(working_text[start:])
                break
            # Append the part before the match.
            parts.append(working_text[start:earliest_index])
            # Append the replacement.
            parts.append(earliest_pair[1])
            # Move start after the matched search string.
            start = earliest_index + earliest_search_len
        # Combine parts.
        return ''.join(parts)
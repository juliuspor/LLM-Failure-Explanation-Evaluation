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

        # Work on mutable copy of text
        result = text
        # We'll process replacements in a loop, scanning from left to right.
        # We need to consider that after a replacement, the new text may have new matches
        # for the same or other search strings that start before the replacement end.
        # The standard algorithm used in Apache Commons Lang (Java) uses a while loop
        # that finds the earliest match among all search strings at each iteration.
        # However, after replacing, it continues searching from the start of the replacement,
        # not from the beginning of the replaced substring. This can miss overlaps.
        # The fix is to restart scanning from the beginning of the replaced substring
        # (i.e., the index where the match started) plus the length of the replacement,
        # but we must also consider that the replacement may contain search strings.
        # Actually, the Java implementation does not restart from the beginning; it continues
        # from after the replacement. Overlaps are not supported. The bug is that the
        # algorithm does not account for the fact that the replacement may have changed
        # the text, so subsequent find operations on the original text are invalid.
        # We need to update the text after each replacement and search again from the
        # position after the replacement.
        # However, the original code uses `text.find` on the original text, which is wrong.
        # We must update `text` (or a mutable copy) after each replacement.
        # Let's implement the correct algorithm:
        # 1. Create a mutable string (we'll use a list of characters or just rebuild string each time).
        # 2. Iterate over the text index from 0.
        # 3. For each position, check each search string to see if it matches at that position.
        # 4. If a match is found, replace it, and move the index to after the replacement.
        # 5. Continue until the end of the string.
        # This is similar to the algorithm used in Apache Commons Lang's replaceEach.
        # However, the original Java implementation uses a while loop that finds the earliest
        # match among all search strings, then replaces, then continues from after the replacement.
        # It does not restart from the beginning of the replaced substring. Overlaps are not handled.
        # The bug in the provided code is that it uses the original `text` for all find operations,
        # ignoring replacements. So we need to update the text after each replacement.
        # Let's fix by building the result incrementally, similar to the original but updating the text.
        # We'll keep a buffer (list of parts) and a current position, but we need to search in the
        # remaining original text? Actually, we need to search in the original text for matches that
        # start at or after the current position, but after a replacement, the original indices shift.
        # The simplest fix is to use a while loop that searches in the original text, but after each
        # replacement, we adjust the start position by the difference in length between the search
        # and replacement strings. However, this is complex because the text changes.
        # Better to rebuild the string step by step, searching in the remaining original substring.
        # We'll keep a variable `current_text` that is the remaining part of the original text that
        # hasn't been processed yet. When we find a match, we append the part before the match and
        # the replacement to the result, and then set `current_text` to the part after the match.
        # Then we continue searching in `current_text`. This way, we don't need to adjust indices.
        # However, we must also consider that matches may overlap across the boundary? No, because
        # we cut off the matched part. Overlaps within the same segment are handled because we
        # always search from the start of `current_text`.
        # Let's implement:
        result_parts = []
        current_text = text
        while True:
            # Find the earliest match among all search strings in current_text
            earliest_index = -1
            replace_idx = -1
            for i in range(search_length):
                search = search_list[i]
                if search is None or len(search) == 0 or replacement_list[i] is None:
                    continue
                pos = current_text.find(search)
                if pos != -1 and (earliest_index == -1 or pos < earliest_index):
                    earliest_index = pos
                    replace_idx = i
            if earliest_index == -1:
                # No more matches
                result_parts.append(current_text)
                break
            # Append the part before the match
            result_parts.append(current_text[:earliest_index])
            # Append the replacement
            result_parts.append(replacement_list[replace_idx])
            # Update current_text to the part after the match
            current_text = current_text[earliest_index + len(search_list[replace_idx]):]
        return "".join(result_parts)
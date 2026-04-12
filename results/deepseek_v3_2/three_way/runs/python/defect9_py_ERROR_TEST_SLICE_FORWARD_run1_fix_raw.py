    @staticmethod
    def replace_each(
        text: Optional[str],
        search_list: Optional[List[Optional[str]]],
        replacement_list: Optional[List[Optional[str]]],
    ) -> Optional[str]:
        """
        Replace multiple search strings in `text`.

        Each entry in `search_list` is replaced by the entry at the same index
        in `replacement_list`. Replacements are applied left-to-right, always
        taking the earliest next match.

        Args:
            text: Input text. If None, returns None.
            search_list: Strings to search for. If None, no replacement is performed.
            replacement_list: Replacement strings corresponding to `search_list`.

        Returns:
            The resulting string with replacements applied.

        Raises:
            ValueError: If `search_list` and `replacement_list` have different lengths.
        """
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

        search_length = len(search_list)
        no_more_matches_for_repl_index = [False] * search_length

        text_index = -1
        replace_index = -1

        # Find the first match (skip null/empty search strings and null replacements).
        for i in range(search_length):
            if (
                no_more_matches_for_repl_index[i]
                or search_list[i] is None
                or len(search_list[i]) == 0
                or replacement_list[i] is None
            ):
                continue
            temp_index = text.find(search_list[i])
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i

        if text_index == -1:
            return text

        # get a good guess on the size of the result buffer so it doesnt have to double if it goes over a bit
        increase = 0

        for i in range(search_length):
            if replacement_list[i] is None or search_list[i] is None:
                continue
            greater = len(replacement_list[i]) - len(search_list[i])
            if greater > 0:
                increase += 3 * greater  # assume 3 matches
        increase = min(increase, len(text) // 5)

        start = 0
        parts: List[str] = []

        while text_index != -1:
            parts.append(text[start:text_index])
            replacement = replacement_list[replace_index]
            if replacement is None:
                # If replacement is None, treat as no replacement (i.e., skip).
                # But we still need to advance start appropriately.
                # However, the search string should not be removed? The spec: if replacement is None, no replacement is done.
                # Actually, the condition above already skips when replacement is None, so replace_index should not point to a None replacement.
                # But to be safe, we can skip appending anything and not advance start? Wait, we already advanced start later.
                # The original code appended replacement even if it's None, causing error.
                # So we should not append None. Instead, we should treat it as if no replacement occurred, meaning we should not replace.
                # But the algorithm already selected this match because replacement was not None (due to earlier check).
                # However, the earlier check only skips if replacement is None when finding matches.
                # So if replacement becomes None after the first match? No, replacement_list is fixed.
                # So we can assert replacement is not None.
                # But to be defensive, we can handle None by not appending and not advancing start? That would break the loop.
                # Instead, we should skip this match entirely and look for the next match.
                # However, that would require re-running the search from the same start.
                # The simplest fix: ensure we never have replace_index pointing to a None replacement.
                # The condition above already ensures that when we set replace_index, replacement_list[i] is not None.
                # So we can safely assume replacement is not None.
                pass
            parts.append(replacement)

            start = text_index + len(search_list[replace_index])

            text_index = -1
            replace_index = -1

            # Find the next earliest match.
            for i in range(search_length):
                if (
                    no_more_matches_for_repl_index[i]
                    or search_list[i] is None
                    or len(search_list[i]) == 0
                    or replacement_list[i] is None
                ):
                    continue
                temp_index = text.find(search_list[i], start)
                if temp_index == -1:
                    no_more_matches_for_repl_index[i] = True
                elif text_index == -1 or temp_index < text_index:
                    text_index = temp_index
                    replace_index = i

        parts.append(text[start:])
        return "".join(parts)
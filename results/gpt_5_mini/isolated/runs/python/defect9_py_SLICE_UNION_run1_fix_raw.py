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

        search_length = len(search_list)
        # track which indices have no more matches
        no_more_matches_for_repl_index = [False] * search_length

        # Find the first match (skip null/empty search strings and null replacements).
        text_index = None
        replace_index = None
        for i in range(search_length):
            s = search_list[i]
            r = replacement_list[i]
            if s is None or len(s) == 0 or r is None:
                no_more_matches_for_repl_index[i] = True
                continue
            temp_index = text.find(s)
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            else:
                if text_index is None or temp_index < text_index:
                    text_index = temp_index
                    replace_index = i

        if text_index is None:
            return text

        # estimate increase
        increase = 0
        for i in range(search_length):
            s = search_list[i]
            # replacement_list has same length, but guard anyway
            r = replacement_list[i] if i < len(replacement_list) else None
            if s is None or r is None:
                continue
            greater = len(r) - len(s)
            if greater > 0:
                increase += 3 * greater
        increase = min(increase, len(text) // 5)

        start = 0
        parts: List[str] = []

        while text_index is not None:
            # append up to match
            parts.append(text[start:text_index])
            parts.append(replacement_list[replace_index])

            # move start past the matched search string
            start = text_index + len(search_list[replace_index])

            # reset for next search
            text_index = None
            replace_index = None

            # find next earliest match after 'start'
            for i in range(search_length):
                if no_more_matches_for_repl_index[i]:
                    continue
                s = search_list[i]
                r = replacement_list[i]
                if s is None or len(s) == 0 or r is None:
                    no_more_matches_for_repl_index[i] = True
                    continue
                temp_index = text.find(s, start)
                if temp_index == -1:
                    no_more_matches_for_repl_index[i] = True
                else:
                    if text_index is None or temp_index < text_index:
                        text_index = temp_index
                        replace_index = i

        parts.append(text[start:])
        return "".join(parts)

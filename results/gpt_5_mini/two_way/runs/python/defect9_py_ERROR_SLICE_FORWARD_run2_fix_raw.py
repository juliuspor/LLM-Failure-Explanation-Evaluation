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
        no_more_matches_for_repl_index = [False] * search_length

        text_index = -1
        replace_index = -1

        for i in range(search_length):
            if no_more_matches_for_repl_index[i]:
                continue
            si = search_list[i]
            ri = replacement_list[i]
            if si is None or len(si) == 0 or ri is None:
                continue
            temp_index = text.find(si)
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i

        if text_index == -1:
            return text

        increase = 0
        for i in range(search_length):
            si = search_list[i]
            ri = replacement_list[i]
            if si is None or ri is None:
                continue
            greater = len(ri) - len(si)
            if greater > 0:
                increase += 3 * greater
        increase = min(increase, len(text) // 5)

        start = 0
        parts: List[str] = []

        while text_index != -1:
            parts.append(text[start:text_index])
            # safe to access replace_index here because text_index != -1 implies replace_index is set
            repl = replacement_list[replace_index]
            parts.append(repl if repl is not None else "")

            si = search_list[replace_index]
            start = text_index + (len(si) if si is not None else 0)

            text_index = -1
            replace_index = -1

            for i in range(search_length):
                if no_more_matches_for_repl_index[i]:
                    continue
                si = search_list[i]
                ri = replacement_list[i]
                if si is None or len(si) == 0 or ri is None:
                    continue
                temp_index = text.find(si, start)
                if temp_index == -1:
                    no_more_matches_for_repl_index[i] = True
                elif text_index == -1 or temp_index < text_index:
                    text_index = temp_index
                    replace_index = i

        parts.append(text[start:])
        return "".join(parts)
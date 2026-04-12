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

    # Pre-filter pairs where search is None/empty or replacement is None, as the original
    # algorithm skips those. This makes later code simpler and safe for len()/indexing.
    filtered_search: List[str] = []
    filtered_replace: List[str] = []
    for s, r in zip(search_list, replacement_list):
        if s is None or len(s) == 0 or r is None:
            continue
        filtered_search.append(s)
        filtered_replace.append(r)

    if not filtered_search:
        return text

    search_length = len(filtered_search)
    no_more_matches_for_repl_index = [False] * search_length

    text_index = -1
    replace_index = -1

    # Find the first match
    for i in range(search_length):
        temp_index = text.find(filtered_search[i])
        if temp_index == -1:
            no_more_matches_for_repl_index[i] = True
        elif text_index == -1 or temp_index < text_index:
            text_index = temp_index
            replace_index = i

    if text_index == -1:
        return text

    # estimate buffer size increase
    increase = 0
    for i in range(search_length):
        greater = len(filtered_replace[i]) - len(filtered_search[i])
        if greater > 0:
            increase += 3 * greater
    increase = min(increase, len(text) // 5)

    start = 0
    parts: List[str] = []

    while text_index != -1:
        parts.append(text[start:text_index])
        parts.append(filtered_replace[replace_index])

        start = text_index + len(filtered_search[replace_index])

        text_index = -1
        replace_index = -1

        # Find next earliest match
        for i in range(search_length):
            if no_more_matches_for_repl_index[i]:
                continue
            temp_index = text.find(filtered_search[i], start)
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i

    parts.append(text[start:])
    return "".join(parts)

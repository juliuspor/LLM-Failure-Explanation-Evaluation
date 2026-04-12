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

    # Filter valid pairs upfront
    valid_pairs = []
    for i in range(len(search_list)):
        search = search_list[i]
        repl = replacement_list[i]
        if search is not None and len(search) > 0 and repl is not None:
            valid_pairs.append((search, repl))

    if not valid_pairs:
        return text

    search_length = len(valid_pairs)
    no_more_matches_for_repl_index = [False] * search_length

    text_index = -1
    replace_index = -1

    # Find the first match
    for i in range(search_length):
        if no_more_matches_for_repl_index[i]:
            continue
        search_str, _ = valid_pairs[i]
        temp_index = text.find(search_str)
        if temp_index == -1:
            no_more_matches_for_repl_index[i] = True
        elif text_index == -1 or temp_index < text_index:
            text_index = temp_index
            replace_index = i

    if text_index == -1:
        return text

    # Calculate buffer size using only valid pairs
    increase = 0
    for search_str, repl_str in valid_pairs:
        greater = len(repl_str) - len(search_str)
        if greater > 0:
            increase += 3 * greater  # assume 3 matches
    increase = min(increase, len(text) // 5)

    start = 0
    parts: List[str] = []

    while text_index != -1:
        search_str, repl_str = valid_pairs[replace_index]
        parts.append(text[start:text_index])
        parts.append(repl_str)

        start = text_index + len(search_str)

        text_index = -1
        replace_index = -1

        # Find the next earliest match
        for i in range(search_length):
            if no_more_matches_for_repl_index[i]:
                continue
            search_str_i, _ = valid_pairs[i]
            temp_index = text.find(search_str_i, start)
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i

    parts.append(text[start:])
    return "".join(parts)
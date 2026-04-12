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
    if len(search_list) != len(replacement_list):
        raise ValueError(
            f"Search and Replace array lengths don't match: {len(search_list)} vs {len(replacement_list)}"
        )

    search_length = len(search_list)
    # Precompute valid pairs (indices) to avoid modifying input lists
    valid_indices: List[int] = []
    for i in range(search_length):
        s = search_list[i]
        r = replacement_list[i]
        if s is None or len(s) == 0 or r is None:
            # Skip invalid pairs: None replacement means no replacement should occur
            continue
        valid_indices.append(i)

    if not valid_indices:
        return text

    # Track which indices have no more matches to skip future finds
    no_more_matches_for_repl_index = {i: False for i in valid_indices}

    # Find first match among valid indices
    text_index = -1
    replace_index = -1
    for i in valid_indices:
        if no_more_matches_for_repl_index[i]:
            continue
        temp_index = text.find(search_list[i])
        if temp_index == -1:
            no_more_matches_for_repl_index[i] = True
        elif text_index == -1 or temp_index < text_index:
            text_index = temp_index
            replace_index = i

    if text_index == -1:
        return text

    parts: List[str] = []
    start = 0

    while text_index != -1:
        parts.append(text[start:text_index])
        parts.append(replacement_list[replace_index])

        start = text_index + len(search_list[replace_index])

        # reset for next search
        text_index = -1
        replace_index = -1

        # search for next earliest match starting from 'start'
        for i in valid_indices:
            if no_more_matches_for_repl_index.get(i, False):
                continue
            temp_index = text.find(search_list[i], start)
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i

    parts.append(text[start:])
    return "".join(parts)
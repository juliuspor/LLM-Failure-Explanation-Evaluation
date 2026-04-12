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
        s = search_list[i]
        r = replacement_list[i]
        if s is None or r is None or len(s) == 0:
            continue
        temp_index = text.find(s)
        if temp_index == -1:
            no_more_matches_for_repl_index[i] = True
        elif text_index == -1 or temp_index < text_index:
            text_index = temp_index
            replace_index = i

    if text_index == -1:
        return text

    increase = 0
    for i in range(search_length):
        s = search_list[i]
        r = replacement_list[i]
        if s is None or r is None:
            continue
        greater = len(r) - len(s)
        if greater > 0:
            increase += 3 * greater
    if len(text) > 0:
        increase = min(increase, len(text) // 5)
    else:
        increase = 0

    start = 0
    parts: List[str] = []

    while text_index != -1:
        parts.append(text[start:text_index])
        parts.append(replacement_list[replace_index] if replacement_list[replace_index] is not None else "")

        start = text_index + len(search_list[replace_index]) if search_list[replace_index] is not None else start

        text_index = -1
        replace_index = -1

        for i in range(search_length):
            if no_more_matches_for_repl_index[i]:
                continue
            s = search_list[i]
            r = replacement_list[i]
            if s is None or r is None or len(s) == 0:
                continue
            temp_index = text.find(s, start)
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i

    parts.append(text[start:])
    return "".join(parts)
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
    pairs = [
        (s, r)
        for s, r in zip(search_list, replacement_list)
        if s is not None and len(s) > 0 and r is not None
    ]
    if not pairs:
        return text
    search_length = len(pairs)
    no_more_matches_for_repl_index = [False] * search_length
    text_index = -1
    replace_index = -1
    for i in range(search_length):
        s, r = pairs[i]
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
        s, r = pairs[i]
        greater = len(r) - len(s)
        if greater > 0:
            increase += 3 * greater
    increase = min(increase, len(text) // 5)
    start = 0
    parts: List[str] = []
    while text_index != -1:
        parts.append(text[start:text_index])
        parts.append(pairs[replace_index][1])
        start = text_index + len(pairs[replace_index][0])
        text_index = -1
        replace_index = -1
        for i in range(search_length):
            if no_more_matches_for_repl_index[i]:
                continue
            s, r = pairs[i]
            temp_index = text.find(s, start)
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i
    parts.append(text[start:])
    return "".join(parts)
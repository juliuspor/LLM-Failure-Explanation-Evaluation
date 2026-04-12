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

    # estimate increase by scanning for up to a limited number of occurrences per search term
    increase = 0
    for i in range(search_length):
        if search_list[i] is None or replacement_list[i] is None:
            continue
        s = search_list[i]
        r = replacement_list[i]
        if len(r) <= len(s):
            continue
        # count up to 3 occurrences as a cheap heuristic
        count = 0
        start_search = 0
        while count < 3:
            idx = text.find(s, start_search)
            if idx == -1:
                break
            count += 1
            start_search = idx + len(s)
        increase += (len(r) - len(s)) * count
    increase = min(increase, len(text) // 5) if len(text) > 0 else 0

    start = 0
    parts: List[str] = []

    while text_index != -1:
        # append text before match and the replacement
        parts.append(text[start:text_index])
        parts.append(replacement_list[replace_index])

        # move start past the matched string
        start = text_index + len(search_list[replace_index])

        # reset for next search
        text_index = -1
        replace_index = -1

        # Find the next earliest match starting from 'start'.
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

        # if no next match found, break out
        if text_index == -1:
            break

    parts.append(text[start:])
    return "".join(parts)
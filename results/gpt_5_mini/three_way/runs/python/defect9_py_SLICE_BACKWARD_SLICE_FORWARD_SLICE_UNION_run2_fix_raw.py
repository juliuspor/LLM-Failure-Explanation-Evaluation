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

    # mark invalid entries (None replacement or None/empty search)
    valid = [True] * search_length
    any_valid = False
    for i in range(search_length):
        if search_list[i] is None or replacement_list[i] is None:
            valid[i] = False
        else:
            # treat empty search string as invalid to avoid infinite loops
            try:
                if len(search_list[i]) == 0:
                    valid[i] = False
            except Exception:
                valid[i] = False
        if valid[i]:
            any_valid = True

    if not any_valid:
        return text

    no_more_matches_for_repl_index = [not v for v in valid]

    text_index = -1
    replace_index = -1

    # Find the first match (skip invalid entries).
    for i in range(search_length):
        if not valid[i]:
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
        if not valid[i]:
            continue
        greater = len(replacement_list[i]) - len(search_list[i])
        if greater > 0:
            increase += 3 * greater  # assume 3 matches
    increase = min(increase, len(text) // 5) if len(text) > 0 else 0

    start = 0
    parts: List[str] = []

    while text_index != -1 and replace_index != -1:
        parts.append(text[start:text_index])
        parts.append(replacement_list[replace_index])

        start = text_index + len(search_list[replace_index])

        text_index = -1
        replace_index = -1

        # Find the next earliest match.
        for i in range(search_length):
            if no_more_matches_for_repl_index[i] or not valid[i]:
                continue
            temp_index = text.find(search_list[i], start)
            if temp_index == -1:
                no_more_matches_for_repl_index[i] = True
            elif text_index == -1 or temp_index < text_index:
                text_index = temp_index
                replace_index = i

    parts.append(text[start:])
    return "".join(parts)
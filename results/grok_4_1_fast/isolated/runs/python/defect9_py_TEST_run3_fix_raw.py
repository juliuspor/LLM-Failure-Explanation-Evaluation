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

    # Filter out invalid pairs (null/empty search or null replacement)
    valid_pairs = []
    for i in range(len(search_list)):
        search = search_list[i]
        repl = replacement_list[i]
        if search is not None and len(search) > 0 and repl is not None:
            valid_pairs.append((search, repl))

    if not valid_pairs:
        return text

    buf: List[str] = []
    pos = 0

    while pos < len(text):
        best_match_len = 0
        best_repl = None
        best_end = pos

        # Check all valid search strings starting at current position
        for search, repl in valid_pairs:
            search_len = len(search)
            if pos + search_len <= len(text) and text[pos:pos + search_len] == search:
                if search_len > best_match_len:
                    best_match_len = search_len
                    best_repl = repl
                    best_end = pos + search_len

        if best_repl is not None:
            # Found a match, append replacement
            buf.append(best_repl)
            pos = best_end
        else:
            # No match, append single character
            buf.append(text[pos])
            pos += 1

    return "".join(buf)
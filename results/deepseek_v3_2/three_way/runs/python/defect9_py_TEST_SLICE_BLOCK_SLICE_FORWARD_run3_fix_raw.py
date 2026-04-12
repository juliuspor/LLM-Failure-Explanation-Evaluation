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

        # Find the first match (skip null/empty search strings, but allow null replacements).
        for i in range(search_length):
            if (
                no_more_matches_for_repl_index[i]
                or search_list[i] is None
                or len(search_list[i]) == 0
            ):
                continue
            # replacement_list[i] can be None, meaning we should still match but not replace.
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
            if replacement_list[i] is None:
                continue
            greater = len(replacement_list[i]) - len(search_list[i])
            if greater > 0:
                increase += 3 * greater  # assume 3 matches
        increase = min(increase, len(text) // 5)

        start = 0
        parts: List[str] = []

        while text_index != -1:
            parts.append(text[start:text_index])
            # replacement_list[replace_index] may be None, meaning we should delete the match.
            # In Java, null replacement means no replacement (i.e., remove).
            # But the spec says: if replacement is null, then no replacement is made.
            # However, the Java implementation treats null as empty string? Let's check.
            # Actually, the Java implementation of replaceEach in StringUtils (Lang 3.9) does:
            # if (searchList[i] == null || replacementList[i] == null) { continue; }
            # So it skips the pair entirely. But the test expects that null replacement means no replacement.
            # Wait, the bug diagnosis says: null replacement should mean no replacement occurs for that search string,
            # but the search string should still be considered for matches.
            # That's contradictory: if we consider the match, what do we replace it with? The original text? That would be no replacement.
            # Actually, the Java implementation's behavior: if replacement is null, the pair is skipped entirely (so no match considered).
            # But the bug diagnosis says that's wrong. Let's re-read: "The intended behavior (based on the Java tests) is that a null replacement should mean no replacement occurs for that search string, but the search string should still be considered for matches."
            # That means we should match the search string, but when we replace, we replace with nothing? Or we skip replacement? The example: search_list ["a", "b"], replacement_list ["c", None], text "aba" -> expected "cbc".
            # Wait, that example: replace "a" with "c", and "b" with None. If None means no replacement, then "b" stays "b". So "aba" -> "cbc". That's exactly what the bug says: current code skips the pair, so "b" is never matched, so "b" stays "b"? Actually, if we skip the pair, we don't match "b" at all, so "b" remains unchanged. That's the same result? No, because if we skip the pair, we never consider "b" as a search string, so we don't replace it with anything, so it stays "b". That's what we want. But the bug says the current code leads to "aca" instead of "cbc". How does that happen? Let's simulate: current code skips pair when replacement is None, so "b" is not in the search list. Then only "a" is replaced with "c", so "aba" -> "cbc"? Wait, "aba" with only replacing "a" with "c" gives "cbc". That's correct. But the bug says output is "aca". That would happen if we incorrectly replaced "b" with something else? Actually, the bug says: "the pair ("b", None) is skipped, so "b" in "aba" is never replaced, resulting in "aca" instead of "cbc"." That doesn't make sense: if "b" is never replaced, it stays "b", so we get "cbc". So why "aca"? Maybe the algorithm incorrectly removes "b" because it matches but replacement is None, and they treat None as empty string? Or maybe the algorithm incorrectly matches "b" and then replaces with empty string? Let's examine the code: In the loop that finds the next replacement, lines 285-288: if replacement_list[i] is None, we skip. That means we don't consider that search string at all. So "b" is not considered. Then only "a" is replaced. So result should be "cbc". But the bug says result is "aca". That suggests that the algorithm is actually removing "b" (replacing with empty string). How could that happen? Look at the replacement step: when we find a match, we do parts.append(replacement_list[replace_index]). If replacement_list[replace_index] is None, we append None? That would cause an error. But the condition above ensures replace_index is only set for pairs where replacement_list[i] is not None. So replace_index will never point to a None replacement. Therefore, the algorithm never selects a match where replacement is None. So "b" is never selected. So why "aca"? Wait, maybe the example is different: text "aba", search_list ["a", "b"], replacement_list ["c", None]. The algorithm first finds the earliest match: "a" at index 0. replace_index=0. Replace with "c". start becomes 1. Then find next match from start=1: text[1:] is "ba". The earliest match? We look for "a" and "b". "b" at index 1 (relative to original text? Actually, we search from start=1. text.find("b",1) returns 1. text.find("a",1) returns 2. So earliest is "b" at index 1. But replacement_list for "b" is None, so we skip it? In the current code, we skip it because replacement_list[i] is None, so we don't consider it. So we don't set text_index to 1. Instead, we consider only "a", which gives index 2. So text_index becomes 2, replace_index becomes 0. Then we replace that "a" with "c". So we replace both "a"s with "c", and "b" is left untouched. That yields "cbc". So why does the bug say "aca"? Maybe the test expects that null replacement means remove (empty string). That would give "aca" (replace "a" with "c", remove "b"). That matches the output "aca". So the intended behavior is: null replacement means replace with empty string (i.e., delete). The bug diagnosis says: "null replacement should mean no replacement occurs for that search string, but the search string should still be considered for matches." That's ambiguous: "no replacement" could mean we don't change the matched substring, i.e., we leave it as is. But the example shows removal. Let's check the Java source. In Apache Commons Lang 3.9, the method replaceEach(String text, String[] searchList, String[] replacementList) has the following behavior: if any search string is null or empty, or any replacement is null, then that pair is skipped entirely. That means null replacement leads to skipping the pair, not deletion. But the test suite might have a different expectation. Actually, the bug report is from a test failure. The test likely expects that null replacement means delete. Let's look at the test case: "test_null_safety_inside_arrays_mixed". It might be from the Apache Commons Lang test suite. I recall that in Commons Lang, replaceEach does treat null replacement as skip, not delete. However, there is also replaceEachRepeatedly that handles null differently? I'm not sure.

Given the bug diagnosis explicitly states: "the intended behavior (based on the Java tests) is that a null replacement should mean no replacement occurs for that search string, but the search string should still be considered for matches." And the example: search_list ["a", "b"], replacement_list ["c", None], text "aba" -> expected "cbc". That means we want "b" to remain "b". So null replacement means we don't replace, i.e., we keep the original substring. But the algorithm currently skips the pair, which also results in keeping the original substring. So why does the test fail? Because the algorithm also skips the pair when finding matches, so "b" is never matched, but that's okay because we don't want to replace it anyway. However, the bug says the output is "aca", which suggests that "b" was removed. That could happen if the algorithm incorrectly treated None as empty string when appending. Let's examine the code after the fix: In the replacement step, we append replacement_list[replace_index]. If replacement_list[replace_index] could be None, we need to handle it. The bug diagnosis says the condition should allow replacement_list[i] to be None but still process the search. That means we should consider matches where replacement is None, and when we replace, we should replace with None? That would cause an error. Actually, we need to decide: what does "no replacement" mean? It could mean we don't change the substring, i.e., we should not perform the replacement at all. That means we should not even consider that search string for replacement, but we should still consider it for matching? That's contradictory. If we consider it for matching, we have to decide what to do when we match. If we don't replace, we should leave the matched substring in place, which is equivalent to not doing anything. That's the same as not considering the search string at all. So why would we need to consider it? Because the order of replacements matters: if we have overlapping patterns, we might need to skip a match because another pattern should take precedence? But the algorithm picks the earliest match. If we have two search strings that match at the same position, we need to decide which one to apply. If one has null replacement, we might want to skip it and apply the other. That's a scenario where considering the search string but with null replacement matters.

Let's think: The algorithm finds the earliest match among all search strings. If a search string has null replacement, we still want to know where it matches, because if it is the earliest, we might decide to do nothing (i.e., not replace), but then we need to move start past that match? Or we should skip that match and look for the next earliest? The Java implementation likely skips the pair entirely, meaning that search string is not considered at all. That would affect the earliest match calculation. For example, suppose text "abc", search strings ["a", "ab"], replacements ["X", None]. If we skip the pair for "ab", we only consider "a", so we replace "a" with "X", resulting "Xbc". If we consider "ab" but with null replacement, we might match "ab" at index 0, and because replacement is null, we do nothing, but then we move start past "ab"? That would skip the "a" replacement. That's different.

Given the bug diagnosis is from the test suite, we should trust it. The fix is to allow replacement_list[i] to be None in the condition, i.e., remove the check for replacement_list[i] is None. That means we will consider matches even when replacement is None. Then, when we actually replace, we need to decide what to do. The Java test expects that null replacement means no replacement, i.e., we should not change the matched substring. But if we don't change it, we should not append anything? Actually, we need to keep the original substring in the output. That means we should not append a replacement; instead, we should leave the matched text as is. But the algorithm currently appends replacement_list[replace_index]. If that is None, we would append None, which is wrong. So we need to handle that: if replacement_list[replace_index] is None, we should not append anything? But we already cut out the matched substring because we added text[start:text_index] and then we would normally add the replacement. If we add nothing, the matched substring is omitted, which would delete it. That's not what we want. We want to keep the matched substring. So we should not cut it out. That means we should not treat it as a replacement at all. So we should skip that match and continue searching from the same start? Or we should move start past the match but also include the matched substring in the output. The simplest is to treat null replacement as a no-op: we should not perform the replacement, but we should still advance start past the match so that we don't match the same substring again. That means we need to include the matched substring in the output. We can do that by not appending a replacement, but we already appended text[start:text_index] which is the part before the match. Then we need to also append the matched substring. So we could append search_list[replace_index] (the matched text) instead of replacement. Then set start = text_index + len(search_list[replace_index]). That would keep the matched text.

Let's implement that: In the while loop, after we find a match at text_index with replace_index, we append text[start:text_index]. Then if replacement_list[replace_index] is None, we append search_list[replace_index] (the matched substring), else we append replacement_list[replace_index]. Then update start.

But we must also adjust the increase calculation: we only need to consider replacements that are not None.

Also, in the initial match-finding loop, we should not skip if replacement is None. So remove the check for replacement_list[i] is None.

Let's code accordingly.

We also need to update the increase calculation to skip None replacements.

Now, we must also consider that search_list[i] could be None or empty; we skip those.

Let's write the fixed code.

We'll keep the same function signature and docstring, but the output format says "Do NOT include a docstring." So we'll omit the docstring? The instruction says: "the complete, fully valid Python code for the fixed `StringUtils.replace_each` only (including decorators if any). Do NOT include a docstring. Do NOT include Markdown fences." So we should output just the method code without the docstring. However, the original code includes a docstring. But the output format says not to include a docstring. I'll remove the docstring and just keep the method body.

We'll output the entire method from @staticmethod to the end.

Let's craft the code accordingly.
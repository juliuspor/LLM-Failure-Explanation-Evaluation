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

        # Convert to list for mutability, and handle None replacements as empty string? 
        # The original algorithm expects None replacements to be skipped, but we already skip them in the loop.
        # We'll keep the same logic.
        
        # We'll use a while loop scanning from left to right, always picking the earliest match.
        # After a replacement, we continue scanning from the position after the replacement string.
        # This ensures overlapping patterns are considered correctly.
        
        # Build a list of (search, replace) pairs, filtering out invalid entries.
        pairs = []
        for i in range(len(search_list)):
            search = search_list[i]
            replace = replacement_list[i]
            if search is None or len(search) == 0 or replace is None:
                # Skip this pair as it won't be matched.
                continue
            pairs.append((search, replace))
        
        if not pairs:
            return text
        
        result_parts = []
        current_pos = 0
        text_len = len(text)
        
        while current_pos < text_len:
            # Find the earliest match among all search strings starting at or after current_pos
            earliest_match_index = -1
            earliest_match_start = text_len  # larger than any possible index
            earliest_search_len = 0
            earliest_replace = None
            
            for search, replace in pairs:
                # Find the next occurrence of search starting at current_pos
                found = text.find(search, current_pos)
                if found != -1 and found < earliest_match_start:
                    earliest_match_start = found
                    earliest_match_index = found
                    earliest_search_len = len(search)
                    earliest_replace = replace
            
            if earliest_match_index == -1:
                # No more matches
                break
            
            # Append the part before the match
            result_parts.append(text[current_pos:earliest_match_start])
            # Append the replacement
            result_parts.append(earliest_replace)
            # Move current position to after the match in the original text? 
            # Actually we need to continue scanning from after the replacement, but since we are building the result incrementally,
            # we can just update current_pos to after the matched substring in the original text.
            # However, overlapping matches could start inside the replaced area? The algorithm should not allow overlapping because
            # we are scanning from left to right and moving past the matched substring. Overlaps that start before the end of the matched substring
            # would have been found earlier (since we pick earliest start). After replacement, we should not re-scan the replaced characters.
            # So we set current_pos = earliest_match_start + earliest_search_len
            current_pos = earliest_match_start + earliest_search_len
        
        # Append the remaining part after the last match
        result_parts.append(text[current_pos:])
        
        return "".join(result_parts)
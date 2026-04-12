    def translate(self, input_seq: Optional[str], out: List[int]) -> None:
        if out is None:
            raise ValueError("The Writer must not be null")
        if input_seq is None:
            return
        code_units = to_utf16_code_units(input_seq)
        pos = 0
        length = len(code_units)
        while pos < length:
            consumed = self.translate_codepoint(code_units, pos, out)
            if consumed == 0:
                # Get the codepoint at current position
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += char_count(codepoint)
                continue
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            # However, the consumed count is in codepoints, not code units.
            # We need to advance pos by the number of code units corresponding to the consumed codepoints.
            # We'll iterate over consumed codepoints, advancing pos by char_count for each.
            for _ in range(consumed):
                codepoint = code_point_at(code_units, pos)
                pos += char_count(codepoint)

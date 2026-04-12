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
                # Get the codepoint and how many code units it occupies in the input
                codepoint = code_point_at(code_units, pos)
                # Determine how many code units were consumed to form this codepoint
                if 0xD800 <= code_units[pos] <= 0xDBFF and pos + 1 < length:
                    low = code_units[pos + 1]
                    if 0xDC00 <= low <= 0xDFFF:
                        # It's a surrogate pair, so consumed 2 code units
                        input_consumed = 2
                    else:
                        input_consumed = 1
                else:
                    input_consumed = 1
                # Output the codepoint as UTF-16 code units
                c = to_chars(codepoint)
                out.extend(c)
                pos += input_consumed
                continue
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            for pt in range(consumed):
                pos += char_count(code_point_at(code_units, pos))
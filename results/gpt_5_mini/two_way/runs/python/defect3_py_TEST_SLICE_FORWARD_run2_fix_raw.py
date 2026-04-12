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
            # Handle surrogate pairs explicitly to ensure correct advancement
            cu = code_units[pos]
            # If it's a high surrogate and followed by a low surrogate, consume both
            if 0xD800 <= cu <= 0xDBFF:
                if pos + 1 < length:
                    low = code_units[pos + 1]
                    if 0xDC00 <= low <= 0xDFFF:
                        out.append(cu)
                        out.append(low)
                        pos += 2
                        continue
                    else:
                        # High surrogate not followed by low surrogate -> invalid
                        raise ValueError(f"Invalid surrogate pair at index {pos}: high surrogate not followed by low surrogate")
                else:
                    # High surrogate at end of input -> invalid
                    raise ValueError(f"Invalid surrogate pair at index {pos}: high surrogate at end of input")
            # If it's a low surrogate without a preceding high surrogate -> invalid
            if 0xDC00 <= cu <= 0xDFFF:
                raise ValueError(f"Invalid low surrogate at index {pos}")

            # Regular BMP character
            out.append(cu)
            pos += 1
            continue

        # If translator consumed codepoints, advance pos by the number of UTF-16 code units
        for _ in range(consumed):
            # Ensure we aren't going out of bounds
            if pos >= length:
                break
            cp = code_point_at(code_units, pos)
            pos += char_count(cp)

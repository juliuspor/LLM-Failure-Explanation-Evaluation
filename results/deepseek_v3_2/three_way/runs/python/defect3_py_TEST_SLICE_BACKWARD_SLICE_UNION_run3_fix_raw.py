    def translate(self, input_seq: Optional[str], out: List[int]) -> None:
        """
        Translate `input_seq` into UTF-16 code units appended to `out`.

        Subclasses customize behavior by implementing `translate_codepoint()`,
        which can consume one or more code points at the current position.

        Args:
            input_seq: Text to translate. If None, nothing is written.
            out: Destination list of UTF-16 code units.
            
        Raises:
            ValueError: If `out` is None.
        """
        if out is None:
            raise ValueError("The Writer must not be null")
        if input_seq is None:
            return
        
        # Convert to UTF-16 code units (simulating Java's char[])
        code_units = to_utf16_code_units(input_seq)
        
        pos = 0
        length = len(code_units)
        
        while pos < length:
            consumed = self.translate_codepoint(code_units, pos, out)
            if consumed == 0:
                # No translation, copy the current code unit(s) as is
                # But we need to copy either a single code unit or a surrogate pair
                # Determine if current position is a high surrogate start of a pair
                if 0xD800 <= code_units[pos] <= 0xDBFF and pos + 1 < length:
                    low = code_units[pos + 1]
                    if 0xDC00 <= low <= 0xDFFF:
                        # Valid surrogate pair
                        out.append(code_units[pos])
                        out.append(low)
                        pos += 2
                        continue
                # Single code unit (BMP or unpaired surrogate)
                out.append(code_units[pos])
                pos += 1
                continue
            
            # consumed > 0: translator handled some codepoints
            # Need to advance pos by the number of UTF-16 code units corresponding to consumed codepoints
            # Since consumed is number of codepoints, we need to convert that to code units
            # We can iterate through the code units from current pos, counting codepoints until we reach consumed
            cp_count = 0
            while cp_count < consumed and pos < length:
                # Determine if current pos is start of a surrogate pair
                if 0xD800 <= code_units[pos] <= 0xDBFF and pos + 1 < length:
                    low = code_units[pos + 1]
                    if 0xDC00 <= low <= 0xDFFF:
                        pos += 2
                        cp_count += 1
                        continue
                # Single code unit
                pos += 1
                cp_count += 1
            # After loop, pos is at next position to process
        
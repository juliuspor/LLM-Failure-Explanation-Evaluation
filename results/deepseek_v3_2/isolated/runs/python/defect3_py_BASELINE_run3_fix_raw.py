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
                # Get the codepoint at current position
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += len(c)
                continue
            
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            # consumed is the number of code units consumed, not code points.
            # However, the method's doc says it returns number of codepoints consumed.
            # We need to convert consumed codepoints to code units.
            # We'll advance pos by the number of code units corresponding to the consumed codepoints.
            # We can compute this by iterating through the consumed codepoints.
            # But a simpler fix: since translate_codepoint already wrote the appropriate code units,
            # we can just advance pos by the number of code units that were part of the consumed codepoints.
            # However, we don't have that information. So we need to change the contract:
            # Let's assume translate_codepoint returns the number of code units consumed.
            # That matches the typical pattern: it processes code_units starting at index.
            # Looking at CsvEscaper, it returns 2 for a surrogate pair (two code units) and 1 for a quote.
            # So indeed, it returns code units consumed.
            # Therefore, we can just do:
            pos += consumed
            
        # Note: The original loop had a for loop that was incorrect.
        # We remove that for loop and just advance pos by consumed.

    def translate(self, input_seq: Optional[str], out: List[int]) -> None:
        if out is None:
            raise ValueError("The Writer must not be null")
        if input_seq is None:
            return
        
        # Convert to UTF-16 code units once
        code_units = to_utf16_code_units(input_seq)
        
        pos = 0  # position in code_units list
        length = len(code_units)
        
        while pos < length:
            consumed = self.translate_codepoint(code_units, pos, out)
            if consumed == 0:
                # No translation, copy the current code unit(s)
                # Determine if it's a high surrogate leading a pair
                high = code_units[pos]
                if 0xD800 <= high <= 0xDBFF and pos + 1 < length:
                    low = code_units[pos + 1]
                    if 0xDC00 <= low <= 0xDFFF:
                        # It's a surrogate pair, copy both
                        out.append(high)
                        out.append(low)
                        pos += 2
                        continue
                # Single code unit (BMP or unpaired surrogate)
                out.append(high)
                pos += 1
                continue
            
            # Translator consumed some code points
            # consumed is number of code points, not code units
            # We need to advance pos by the corresponding number of code units
            # Since translators are expected to understand codepoints, they should
            # have consumed whole surrogate pairs as needed.
            # We can advance by iterating over consumed codepoints.
            # But we don't have direct mapping from code points to code units.
            # Instead, we can rely on the contract that translators return the number
            # of code points consumed, and they must have processed the correct
            # number of code units. However, we don't know how many code units that is.
            # The original code attempted to compute charCount for each consumed
            # codepoint, but that required calling code_point_at again, which is
            # problematic because pos is in code units, not string indices.
            # Actually, the translator's translate_codepoint receives code_units and index
            # (which is a code unit index). It returns the number of codepoints consumed.
            # To advance pos, we need to know how many code units those codepoints occupy.
            # Since the translator already processed them, we can ask it to tell us?
            # But the API doesn't provide that. The original Java implementation likely
            # uses the fact that translate_codepoint returns the number of characters
            # (code units) consumed? Wait, looking at the Java source: 
            # abstract int translate(CharSequence input, int index, Writer out) throws IOException;
            # Returns: number of characters consumed
            # In Java, CharSequence is indexed by char (code unit). So the return is code units.
            # In our Python adaptation, we changed to codepoints? The doc says "number of codepoints consumed".
            # That's the bug: we should return number of code units consumed, not codepoints.
            # Because the index is into code_units list. So if a translator processes a surrogate pair,
            # it should return 2 (code units), not 1 (codepoint).
            # However, the existing CsvEscaper returns 2 for surrogate pair (see its code).
            # It returns 2 because it writes both code units and returns 2.
            # That matches code units. But the doc says codepoints.
            # Let's check the original code's loop after consumed != 0:
            # for pt in range(consumed):
            #     pos += char_count(code_point_at(code_units, pos))
            # This assumes consumed is number of codepoints, and it advances by charCount for each.
            # But code_point_at expects an index into code_units, and pos is already a code unit index.
            # However, code_point_at is called with code_units and pos, which is correct.
            # The problem is that code_point_at uses to_utf16_code_units(s) inside it, but we are passing code_units.
            # Wait, the bug diagnosis says code_point_at uses to_utf16_code_units(s) where s is the original string.
            # Actually, in the provided code, code_point_at takes a list of code units, not a string.
            # The diagnosis is based on a different version? Let's re-examine the given source code.
            # The function code_point_at(code_units: List[int], index: int) -> int uses the list directly.
            # It does not call to_utf16_code_units. So the diagnosis is inaccurate for this version.
            # However, the bug may still exist because the translate method uses code_point_at with code_units,
            # but the index pos is a code unit index, which is fine. The loop after consumed != 0 iterates over
            # consumed codepoints and advances pos by char_count of each codepoint. But if consumed is 1 for a
            # surrogate pair, then char_count would be 2, so pos increases by 2, which is correct.
            # However, the translator (CsvEscaper) returns 2 for a surrogate pair, not 1. So consumed is 2.
            # Then the loop iterates over 2 codepoints? That's wrong because a surrogate pair is one codepoint.
            # The translator should return 1 codepoint consumed, but it returns 2 code units.
            # This mismatch is the core issue.
            # We need to decide the contract: should translate_codepoint return code units or codepoints?
            # Looking at the Java source of CharSequenceTranslator (from Apache Commons Text):
            #   int translate(CharSequence input, int index, Writer out) throws IOException;
            #   Returns: number of characters consumed
            # In Java, CharSequence is indexed by char (UTF-16 code unit). So the return is number of chars (code units).
            # Therefore, our Python adaptation should also return number of code units consumed.
            # Let's change the docstring and the loop accordingly.
            # But we must also adjust the loop for consumed == 0: currently it uses to_chars and char_count.
            # That also uses codepoint functions, but we can avoid that by directly copying code units.
            # Since we have code_units list, we can simply copy the current code unit(s) based on surrogate detection.
            # For consumed != 0, we can just add consumed to pos, because consumed is already the number of code units processed.
            # However, the existing translators (CsvEscaper) return 2 for a surrogate pair, which is code units.
            # That's good. But the doc says codepoints. We'll change the doc to say code units.
            # Also, the loop after consumed != 0 should be: pos += consumed
            # Because the translator already consumed that many code units.
            # Let's implement that fix.
            
            # Fix: assume consumed is number of code units consumed.
            pos += consumed

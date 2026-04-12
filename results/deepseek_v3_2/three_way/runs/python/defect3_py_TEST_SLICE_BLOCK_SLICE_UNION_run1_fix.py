# -*- coding: utf-8 -*-
"""
CharSequenceTranslator - An API for translating text.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


def to_utf16_code_units(s: str) -> List[int]:
    """Convert a Python string to a list of UTF-16 code units (like Java's char[])."""
    code_units = []
    for char in s:
        codepoint = ord(char)
        if codepoint > 0xFFFF:
            # Encode as surrogate pair (like Java)
            codepoint -= 0x10000
            high = 0xD800 + (codepoint >> 10)
            low = 0xDC00 + (codepoint & 0x3FF)
            code_units.append(high)
            code_units.append(low)
        else:
            code_units.append(codepoint)
    return code_units


def code_point_at(code_units: List[int], index: int) -> int:
    """
    Get the Unicode codepoint at the given index in a list of UTF-16 code units.
    Equivalent to Java's Character.codePointAt().
    
    Raises:
        IndexError: if index is out of range
    """
    if index < 0 or index >= len(code_units):
        raise IndexError(f"String index out of range: {index}")
    
    high = code_units[index]
    if 0xD800 <= high <= 0xDBFF and index + 1 < len(code_units):
        low = code_units[index + 1]
        if 0xDC00 <= low <= 0xDFFF:
            # Valid surrogate pair
            return 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
    return high


def char_count(codepoint: int) -> int:
    """
    Returns the number of UTF-16 code units needed to represent a codepoint.
    Equivalent to Java's Character.charCount().
    """
    return 2 if codepoint > 0xFFFF else 1


def to_chars(codepoint: int) -> List[int]:
    """
    Convert a codepoint to UTF-16 code units.
    Equivalent to Java's Character.toChars().
    """
    if codepoint > 0xFFFF:
        codepoint -= 0x10000
        return [0xD800 + (codepoint >> 10), 0xDC00 + (codepoint & 0x3FF)]
    return [codepoint]


class CharSequenceTranslator(ABC):
    """
    An API for translating text.
    Its core use is to escape and unescape text. Because escaping and unescaping
    is completely contextual, the API does not present two separate signatures.
    """
    
    @abstractmethod
    def translate_codepoint(self, code_units: List[int], index: int, out: List[int]) -> int:
        """
        Translate a set of codepoints, represented by an int index into a list of code units,
        into another set of codepoints. The number of codepoints consumed must be returned.
        
        Args:
            code_units: List of UTF-16 code units being translated
            index: int representing the current point of translation
            out: List to append translated code units to
            
        Returns:
            int count of codepoints consumed
        """
        pass
    
    def translate_string(self, input_seq: Optional[str]) -> Optional[str]:
        """
        Helper for non-Writer usage.
        
        Args:
            input_seq: String to be translated
            
        Returns:
            String output of translation
        """
        if input_seq is None:
            return None
        out: List[int] = []
        self.translate(input_seq, out)
        # Convert code units back to string
        result = []
        i = 0
        while i < len(out):
            if 0xD800 <= out[i] <= 0xDBFF and i + 1 < len(out):
                if 0xDC00 <= out[i + 1] <= 0xDFFF:
                    # Surrogate pair
                    codepoint = 0x10000 + ((out[i] - 0xD800) << 10) + (out[i + 1] - 0xDC00)
                    result.append(chr(codepoint))
                    i += 2
                    continue
            result.append(chr(out[i]))
            i += 1
        return ''.join(result)
    
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
    
    def with_translators(self, *translators: 'CharSequenceTranslator') -> 'CharSequenceTranslator':
        """
        Helper method to create a merger of this translator with another set of
        translators. Useful in customizing the standard functionality.
        
        Args:
            translators: CharSequenceTranslator array of translators to merge with this one
            
        Returns:
            CharSequenceTranslator merging this translator with the others
        """
        new_array = [self] + list(translators)
        return AggregateTranslator(new_array)
    
    @staticmethod
    def hex(codepoint: int) -> str:
        """
        Returns an upper case hexadecimal string for the given character.
        
        Args:
            codepoint: The codepoint to convert.
            
        Returns:
            An upper case hexadecimal string
        """
        return format(codepoint, 'X')


class AggregateTranslator(CharSequenceTranslator):
    """
    Aggregates multiple CharSequenceTranslators.
    """
    
    def __init__(self, translators: List[CharSequenceTranslator]):
        self._translators = translators
    
    def translate_codepoint(self, code_units: List[int], index: int, out: List[int]) -> int:
        for translator in self._translators:
            consumed = translator.translate_codepoint(code_units, index, out)
            if consumed != 0:
                return consumed
        return 0


class CsvEscaper(CharSequenceTranslator):
    """
    A translator that escapes strings for CSV format.
    
    This simulates StringEscapeUtils.escapeCsv() behavior.
    """
    
    def translate_codepoint(self, code_units: List[int], index: int, out: List[int]) -> int:
        """
        Escape CSV special characters.
        Returns the number of codepoints consumed.
        """
        code_unit = code_units[index]
        
        # Check if this is a high surrogate (start of surrogate pair)
        if 0xD800 <= code_unit <= 0xDBFF:
            if index + 1 < len(code_units):
                low = code_units[index + 1]
                if 0xDC00 <= low <= 0xDFFF:
                    # Valid surrogate pair - write both code units
                    out.append(code_unit)
                    out.append(low)
                    return 2
        
        # Handle quote escaping: " -> ""
        if code_unit == ord('"'):
            out.append(ord('"'))
            out.append(ord('"'))
            return 1
        
        # No translation needed for other characters
        return 0
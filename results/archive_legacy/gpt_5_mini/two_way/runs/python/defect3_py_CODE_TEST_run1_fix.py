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
        code_units = to_utf16_code_units(input_seq)
        pos = 0
        length = len(code_units)
        while pos < length:
            consumed = self.translate_codepoint(code_units, pos, out)
            if consumed == 0:
                codepoint = code_point_at(code_units, pos)
                c = to_chars(codepoint)
                out.extend(c)
                pos += len(c)
                continue
            if consumed < 0:
                raise ValueError("translate_codepoint returned negative consumed value")
            try:
                advance = 0
                for _ in range(consumed):
                    if pos >= length:
                        break
                    cp = code_point_at(code_units, pos)
                    advance += char_count(cp)
                    pos += char_count(cp)
                if advance == 0:
                    if consumed <= length - pos:
                        pos += consumed
                    else:
                        pos = length
            except IndexError:
                if consumed <= length - pos:
                    pos += consumed
                else:
                    pos = length
        return
    
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

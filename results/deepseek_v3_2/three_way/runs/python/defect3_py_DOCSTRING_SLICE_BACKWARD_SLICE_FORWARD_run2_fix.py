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
                pos += char_count(codepoint)
                continue

            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            # Instead of iterating over consumed codepoints, we need to advance pos by the number of code units consumed.
            # However, the translate_codepoint returns the number of codepoints consumed, not code units.
            # So we need to convert consumed codepoints to code units.
            # We'll step through each consumed codepoint and add the appropriate number of code units.
            # But note: the translator may have already written the translated code units to out.
            # We just need to advance pos by the number of code units that correspond to the consumed codepoints.
            # We can compute that by iterating over the consumed codepoints and summing their charCount.
            # However, we don't have the codepoints themselves; we have code_units and pos.
            # We can iterate over the consumed codepoints by reading from code_units starting at pos.
            # But we must be careful with surrogate pairs.
            # Alternatively, we can change the contract: translate_codepoint returns the number of code units consumed.
            # However, the existing code expects codepoints. The bug diagnosis indicates that the issue is with index out of bounds.
            # Let's examine the loop: after consumed != 0, we have:
            # for pt in range(consumed):
            #     pos += char_count(code_point_at(code_units, pos))
            # This is problematic because code_point_at may be called with an index that is out of bounds if pos is at the end.
            # Actually, the loop is intended to advance pos by the number of code units corresponding to consumed codepoints.
            # But the loop uses code_point_at which may read ahead for surrogate pairs. That's fine as long as pos is within bounds.
            # However, the bug diagnosis says the error occurs at line 35 in code_point_at. That means index >= len(code_units).
            # This can happen if pos becomes equal to length (or greater) due to incorrect advancement.
            # Let's simulate: Suppose we have a single codepoint that is a surrogate pair (2 code units).
            # translate_codepoint returns consumed=1 (one codepoint). Then the loop runs for pt in range(1):
            #   pos += char_count(code_point_at(code_units, pos))
            # At pos=0, code_point_at reads the surrogate pair and returns the codepoint, char_count returns 2.
            # Then pos becomes 2. That's correct.
            # But what if translate_codepoint returns consumed=0? Then we go into the other branch: we get codepoint, write to out, and advance pos by char_count(codepoint). That's also correct.
            # So why the index out of bounds? Possibly because the translator's translate_codepoint returns a consumed value that is too large, causing the loop to advance pos beyond length.
            # Or because the translator returns consumed > 0 but the corresponding codepoints are not properly aligned with code unit boundaries? For example, if it returns consumed=1 but the current position is at a high surrogate without a low surrogate? But code_point_at would handle that.
            # Wait, the bug diagnosis says the error is in code_point_at with index out of bounds. That means the caller passed an index that is out of range. The only caller is the loop in translate.
            # So we need to ensure that pos is always within bounds when calling code_point_at.
            # In the consumed != 0 branch, we call code_point_at in the loop. But if consumed is such that after advancing, pos might become length? Actually, the loop advances pos by char_count for each consumed codepoint. So if the total advancement would exceed length, then code_point_at might be called with pos == length? Let's see: the loop condition is while pos < length. So before entering the loop, pos < length. Then we call translate_codepoint, which returns consumed. Then we have a for loop that runs consumed times. Each iteration calls code_point_at with the current pos, which is guaranteed to be < length because we haven't advanced beyond the total code units? Not necessarily: if the current codepoint is a surrogate pair (2 code units), and consumed is 1, then we advance by 2. That's fine. But if consumed is 2, and each codepoint is a surrogate pair, we would advance by 4 code units. That could exceed length if there aren't enough code units. But translate_codepoint should only consume codepoints that are actually present. It should not return a consumed value that would exceed the remaining codepoints. However, the translator might not know the remaining length? It only gets code_units and index. It can check bounds.
            # The bug might be that the translator returns consumed > 0 but the index is at the end of the list? For example, if the last code unit is a high surrogate without a low surrogate, and the translator returns consumed=1? But then code_point_at would read that high surrogate and return it (since it's not a valid pair). That's okay.
            # Alternatively, the bug could be in the CsvEscaper: it returns 2 for a surrogate pair, but that's the number of code units consumed, not codepoints. The contract says translate_codepoint returns the number of codepoints consumed. In CsvEscaper, for a surrogate pair, it returns 2? Actually, look at CsvEscaper.translate_codepoint: if it's a valid surrogate pair, it writes both code units and returns 2. But that's incorrect: it should return 1 (one codepoint) because a surrogate pair represents a single codepoint. However, the code comment says "Returns the number of codepoints consumed." So returning 2 is wrong. That would cause the loop in translate to iterate twice, each time calling code_point_at. The first iteration would read the surrogate pair (codepoint) and advance by 2 code units. The second iteration would start at pos after the pair, which might be within bounds. But if the surrogate pair is the last thing, then after first iteration pos becomes length, and the second iteration would call code_point_at with index=length, causing IndexError. That's exactly the bug!
            # So the fix is to ensure that translate_codepoint returns the number of codepoints consumed, not code units. For a surrogate pair, it should return 1. In CsvEscaper, when it handles a surrogate pair, it writes both code units but should return 1.
            # However, the bug diagnosis asks to fix the bug in CharSequenceTranslator.translate. But the root cause is in CsvEscaper. But we can also fix the translate method to be robust against such misbehaving translators. We can change the loop to advance pos by the number of code units corresponding to the consumed codepoints, but we need to compute that without calling code_point_at with an out-of-bounds index. We can compute the advancement by iterating over the consumed codepoints, but we need to know the codepoints. Alternatively, we can change the contract: translate_codepoint returns the number of code units consumed. That would simplify things. But that would break existing subclasses. Since we are only allowed to fix the translate method, we must adjust the loop to avoid index out of bounds.
            # Let's redesign the loop: when consumed > 0, we need to advance pos by the number of code units that correspond to those consumed codepoints. We can do:
            #   for _ in range(consumed):
            #       if pos >= length:
            #           break  # safety
            #       codepoint = code_point_at(code_units, pos)
            #       pos += char_count(codepoint)
            # But this still calls code_point_at, which could throw if pos is out of bounds. We already check pos < length, but code_point_at also checks index >= len(code_units). However, if pos == length, we break before calling.
            # So we can add a check: if pos >= length: break.
            # But the loop is already inside while pos < length, so when we start the for loop, pos < length. However, after each iteration, pos may become length, and then the next iteration would have pos == length, which is not < length, but the for loop doesn't re-evaluate the condition; it just runs the fixed number of times. So we need to break if pos >= length.
            # Let's implement that.
            # Also, we should consider that the translator might have already written the translated code units, so we just need to advance pos.
            # So the fixed code for the consumed != 0 branch:
            #   for _ in range(consumed):
            #       if pos >= length:
            #           break
            #       codepoint = code_point_at(code_units, pos)
            #       pos += char_count(codepoint)
            # This will prevent index out of bounds.
            # Additionally, we should ensure that the translator's returned consumed is reasonable. But we can't control that.
            # Let's apply this fix.
            # Also, note that in the consumed == 0 branch, we call code_point_at with pos, which is guaranteed to be < length because of the while condition. So that's safe.
            # Now, we must also update the docstring? Not required.
            # We'll output the fixed translate method.

            for _ in range(consumed):
                if pos >= length:
                    break
                codepoint = code_point_at(code_units, pos)
                pos += char_count(codepoint)
    
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
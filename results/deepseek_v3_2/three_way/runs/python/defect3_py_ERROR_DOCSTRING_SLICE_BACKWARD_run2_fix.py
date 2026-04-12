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

            # Move pos forward by the number of code units consumed
            # The contract of translate_codepoint is that it returns the number of codepoints consumed,
            # not the number of code units. We need to convert codepoints to code units.
            # However, the current implementation incorrectly assumes each codepoint corresponds to one code unit.
            # We need to advance pos by the total code units for the consumed codepoints.
            # We can iterate over the consumed codepoints and add charCount for each.
            # But we don't have the exact codepoints that were consumed; we only have the code_units list.
            # So we need to advance pos by the number of code units that correspond to the consumed codepoints.
            # Since we know the starting position, we can compute the total code units for the first 'consumed' codepoints.
            # Let's implement a helper to compute code unit length for a given number of codepoints from a position.
            # However, the bug diagnosis indicates an IndexError when accessing code_units at index 2.
            # This likely happens in the loop below: for pt in range(consumed): pos += char_count(code_point_at(code_units, pos))
            # The issue is that code_point_at may be called with an index that is out of bounds because pos may be at the end.
            # Specifically, if consumed > 0, we enter the loop. The loop iterates over consumed codepoints.
            # For each iteration, we call code_point_at(code_units, pos). But if pos is already at the last code unit,
            # and that code unit is a high surrogate (needing a low surrogate), code_point_at will try to access index+1.
            # However, the translator's translate_codepoint may have consumed a surrogate pair (2 code units) but returned consumed=1 (codepoint).
            # The current loop then increments pos by charCount (which is 2 for surrogate pair) but we already consumed two code units.
            # This leads to double counting and eventually an out-of-bounds access.
            # The correct approach: after translate_codepoint returns consumed > 0, we should advance pos by the number of code units that correspond to those consumed codepoints.
            # We can compute this by iterating from the current pos, counting codepoints until we have consumed the required number, and summing the charCount for each.
            # Let's implement:
            #   remaining = consumed
            #   while remaining > 0:
            #       codepoint = code_point_at(code_units, pos)
            #       pos += char_count(codepoint)
            #       remaining -= 1
            # But note: code_point_at already handles surrogate pairs and returns the codepoint, and char_count returns 1 or 2.
            # This is exactly what the original loop does, but the original loop uses the same pos variable that is also used in the while condition.
            # The bug is that the loop may call code_point_at with pos that is at the end of the list? Actually, the loop condition ensures pos < length.
            # However, if consumed is incorrectly large, we might exceed length. But the translator should not return consumed more than the remaining codepoints.
            # The bug diagnosis says the IndexError occurs at index 2. Let's examine the specific case: input_seq is short, say "A".
            # code_units = [65] (length 1). pos starts at 0. translate_codepoint returns 0 (since not a quote). Then we go to the if consumed==0 branch.
            # codepoint = code_point_at(code_units, 0) -> returns 65. c = to_chars(65) -> [65]. out.extend([65]), pos += 1 -> pos=1.
            # Loop ends because pos=1 not < length=1. So no error.
            # Now consider input_seq = '"', which is a quote. code_units = [34] (length 1). pos=0. translate_codepoint returns 1 (since it handles quote).
            # Then we go to the else branch. The loop: for pt in range(consumed): pos += char_count(code_point_at(code_units, pos))
            # First iteration: pt=0, code_point_at(code_units, pos=0) -> returns 34, char_count(34)=1, pos becomes 1.
            # Loop ends because consumed=1. Now pos=1, while condition pos < length? length=1, so pos=1 is not less than length, loop ends.
            # No error.
            # Now consider a surrogate pair: input_seq = '\U0001F600' (grinning face). code_units = [55357, 56832] (length 2).
            # pos=0. translate_codepoint: code_units[0] is high surrogate? Actually, code_units[0]=55357 (0xD83D) is high surrogate, code_units[1]=56832 (0xDE00) is low surrogate.
            # In CsvEscaper.translate_codepoint, it checks if high surrogate and if low surrogate exists. It will write both code units and return 2.
            # Then in translate, consumed=2. Then we go to the else branch. Loop: for pt in range(2):
            #   pt=0: code_point_at(code_units, pos=0) -> returns codepoint 128512 (since surrogate pair), char_count returns 2, pos becomes 2.
            #   pt=1: code_point_at(code_units, pos=2) -> IndexError because index=2 >= length=2.
            # The problem: the translator returned consumed=2 (codepoints) but actually it consumed only one codepoint (the surrogate pair).
            # The contract of translate_codepoint is to return the number of codepoints consumed, not code units.
            # In CsvEscaper, for a surrogate pair, it writes both code units and returns 2. But that 2 is the number of code units, not codepoints.
            # The translator should return 1 codepoint consumed for a surrogate pair, because the surrogate pair represents a single codepoint.
            # However, the CsvEscaper's translate_codepoint returns 2 when it handles a surrogate pair. That's wrong.
            # But the bug diagnosis says the error is in CharSequenceTranslator.translate, not in CsvEscaper. However, the bug is triggered by CsvEscaper's behavior.
            # We need to fix the translate method to handle the case where translate_codepoint returns the number of code units consumed, not codepoints.
            # Actually, the documentation says translate_codepoint returns the number of codepoints consumed. So CsvEscaper is buggy.
            # But we are only allowed to fix the translate method. The bug diagnosis says the error occurs because of an index out of range in translate.
            # So we need to make translate robust even if translate_codepoint returns an incorrect count.
            # We can change the loop to advance pos by the number of code units that correspond to the consumed codepoints, but we must ensure we don't go out of bounds.
            # We can compute the advance by iterating over the consumed codepoints, but we need to know the exact codepoints. Instead, we can use the fact that the translator has already written the appropriate code units to out, and we just need to skip the corresponding code units in the input.
            # A safer approach: after translate_codepoint returns consumed > 0, we should advance pos by the number of code units that were consumed by the translator. However, the translator does not tell us that.
            # Alternatively, we can change the contract: translate_codepoint should return the number of code units consumed, not codepoints. But that would break other subclasses.
            # Looking at the original Java code (Apache Commons Text), the translate method uses the codepoint approach. The bug might be in the loop: the loop increments pos by charCount for each consumed codepoint, but it uses the current pos which may have been advanced by the previous iteration. However, the loop variable pt is not used. The loop should be:
            #   for (int pt = 0; pt < consumed; pt++) {
            #       pos += Character.charCount(Character.codePointAt(input, pos));
            #   }
            # This is exactly what we have. The issue is that if consumed is greater than the number of codepoints remaining, we get an error.
            # In the surrogate pair case, consumed should be 1, not 2. So the fix is to ensure that translate_codepoint returns the correct number of codepoints.
            # But we are only to fix the translate method. So we need to adjust the loop to not exceed the length of code_units.
            # We can change the loop to while consumed > 0 and pos < length:
            #   codepoint = code_point_at(code_units, pos)
            #   pos += char_count(codepoint)
            #   consumed -= 1
            # This ensures we stop if we run out of code units.
            # However, if consumed is too large, we may still leave some code units unprocessed? But the translator should have consumed exactly the code units corresponding to the codepoints. If consumed is too large, we will skip more than we should. But that's a bug in the translator.
            # To prevent IndexError, we can add a bounds check in the loop.
            # Let's implement:
            #   for _ in range(consumed):
            #       if pos >= length:
            #           break
            #       codepoint = code_point_at(code_units, pos)
            #       pos += char_count(codepoint)
            # This will break if pos goes out of bounds, but then the outer while loop will also exit because pos >= length.
            # However, if we break early, consumed is not fully accounted for, but that's okay because we have reached the end.
            # But the translator might have written output for codepoints that don't exist? That's a translator bug.
            # Given the bug diagnosis, the immediate fix is to prevent the IndexError. So we add a guard in the loop.
            # Alternatively, we can compute the maximum possible codepoints from the current position: max_codepoints = number of codepoints from pos to end.
            # But that's complex.
            # Let's implement the guard.
            # Also, note that the loop uses code_point_at which may itself raise IndexError if pos is at the last code unit and it's a high surrogate without a low surrogate. But code_point_at already handles that and returns the high surrogate as the codepoint (since it's not a valid pair). That's fine.
            # So the fix: replace the for loop with a while loop that respects remaining consumed and pos < length.
            # We'll keep the same logic but with a guard.
            # Code:
            remaining = consumed
            while remaining > 0 and pos < length:
                codepoint = code_point_at(code_units, pos)
                pos += char_count(codepoint)
                remaining -= 1
            # If remaining > 0, we consumed less than the translator claimed, but that's okay.
            # Then continue the outer loop.
            # This should prevent IndexError.
            # Let's write the fixed method accordingly.
            remaining = consumed
            while remaining > 0 and pos < length:
                codepoint = code_point_at(code_units, pos)
                pos += char_count(codepoint)
                remaining -= 1
    
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
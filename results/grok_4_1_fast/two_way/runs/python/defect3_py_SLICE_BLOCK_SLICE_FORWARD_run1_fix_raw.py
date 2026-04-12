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
    if 0xD800 <= high <= 0xDBFF:
        if index + 1 >= len(code_units):
            raise IndexError("Malformed UTF-16: lone high surrogate")
        low = code_units[index + 1]
        if 0xDC00 <= low <= 0xDFFF:
            # Valid surrogate pair
            return 0x10000 + ((high - 0xD800) << 10) + (low - 0xDC00)
        else:
            raise IndexError("Malformed UTF-16: high surrogate not followed by low surrogate")
    return high

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
                pos += len(c)
                continue
            
            # Contract with translators is that they have to understand codepoints
            # and they just took care of a surrogate pair
            for pt in range(consumed):
                pos += char_count(code_point_at(code_units, pos))
    
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
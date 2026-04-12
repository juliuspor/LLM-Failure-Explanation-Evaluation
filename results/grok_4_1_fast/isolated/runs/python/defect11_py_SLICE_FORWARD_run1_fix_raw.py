@staticmethod
def random(count: int, start: int = 0, end: int = 0, letters: bool = False, numbers: bool = False) -> str:
    """
    Creates a random string based on a variety of options.

    The character range is defined by the half-open interval `[start, end)`.
    If `letters` is True, generated characters are restricted to alphabetic
    characters; if `numbers` is True, they are restricted to digits.

    Args:
        count: Length of the generated string.
        start: Lower bound (inclusive) of the character range.
        end: Upper bound (exclusive) of the character range.
        letters: Whether to restrict output to letters.
        numbers: Whether to restrict output to numbers.

    Returns:
        A randomly generated string of length `count`.
    """
    if count == 0:
        return ""
    if count < 0:
        raise ValueError(f"Requested random string length {count} is less than 0.")
    
    # Derive default character range
    if start == 0 and end == 0:
        if letters or numbers:
            end = ord('z') + 1
            start = ord(' ')
        else:
            end = 127
            start = 32  # Printable ASCII
    
    if end <= start:
        raise ValueError(f"Invalid range: start={start}, end={end}")
    
    gap = end - start
    buffer: list[str] = [''] * count
    pos = count - 1
    attempts = 0
    max_attempts = count * 10  # Prevent infinite loops
    
    while pos >= 0 and attempts < max_attempts:
        code_point = start + _next_int_java(_RANDOM, gap)
        ch = chr(code_point)
        
        accepted = (letters and ch.isalpha()) or (numbers and ch.isdigit()) or \
                   (not letters and not numbers)
        
        if not accepted:
            attempts += 1
            continue
        
        code_point = ord(ch)
        
        if _is_low_surrogate(code_point):
            if pos == 0:
                attempts += 1
                continue
            buffer[pos] = ch
            pos -= 1
            # Generate matching high surrogate
            buffer[pos] = chr(55296 + _next_int_java(_RANDOM, 128))
            pos -= 1
            attempts += 1
            continue
        
        if _is_high_surrogate(code_point):
            if pos == 0:
                attempts += 1
                continue
            buffer[pos] = chr(56320 + _next_int_java(_RANDOM, 128))
            pos -= 1
            buffer[pos] = ch
            pos -= 1
            attempts += 1
            continue
        
        if _is_private_high_surrogate(code_point):
            attempts += 1
            continue
        
        buffer[pos] = ch
        pos -= 1
        attempts += 1
    
    if pos >= 0:
        raise ValueError(f"Could not generate enough valid characters after {max_attempts} attempts")
    
    return ''.join(buffer)

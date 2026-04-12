    @staticmethod
    def random(count: int, start: int, end: int, letters: bool, numbers: bool) -> str:
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
        if start == 0 and end == 0:
            # No explicit range, use default behavior
            return RandomStringUtils._random_internal(
                count=count,
                start=start,
                end=end,
                letters=letters,
                numbers=numbers,
                chars=None,
                rnd=_RANDOM,
            )
        # Validate that the range is not empty
        if end <= start:
            raise ValueError(f"Invalid range: start={start}, end={end} (must be start < end)")
        # If both letters and numbers are False, we accept any character in range.
        # If letters or numbers is True, we need to ensure at least one character in range matches.
        # We'll let _random_internal handle the generation; it will loop until it finds acceptable characters.
        # However, to avoid infinite loops, we must ensure there is at least one acceptable character.
        # We'll compute the set of acceptable code points in the range.
        acceptable = []
        for code_point in range(start, end):
            ch = chr(code_point)
            if (letters and ch.isalpha()) or (numbers and ch.isdigit()) or (not letters and not numbers):
                acceptable.append(code_point)
        if not acceptable:
            raise ValueError("No valid characters in the specified range with the given constraints.")
        # Now we know there is at least one acceptable character, so we can proceed.
        # But we cannot pass the filtered list directly because _random_internal expects a range.
        # We'll still call _random_internal with the original range; it will loop but eventually find one.
        # However, to be efficient and avoid long loops, we can pass a custom chars list.
        # Let's create a list of acceptable characters and pass it as chars.
        chars = [chr(c) for c in acceptable]
        return RandomStringUtils._random_internal(
            count=count,
            start=0,
            end=len(chars),
            letters=False,  # Already filtered
            numbers=False,  # Already filtered
            chars=chars,
            rnd=_RANDOM,
        )
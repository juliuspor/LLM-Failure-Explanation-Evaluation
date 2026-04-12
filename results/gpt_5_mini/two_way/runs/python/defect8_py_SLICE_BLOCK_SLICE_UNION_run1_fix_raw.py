@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # Must be at least 2 (language) and if longer follow patterns
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Validate language (first two chars must be lowercase letters)
        if length >= 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 2:
            return Locale(locale_str, "")

        # From here on, must have '_' at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Need at least positions 3 and 4 for country
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")

        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])

        # length > 5: must have '_' at position 5 and a variant following
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # variant may be empty string? In Java variant must exist if underscore present; require at least one char
        if length == 6:
            # No variant characters after the underscore
            raise ValueError(f"Invalid locale format: {locale_str}")

        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
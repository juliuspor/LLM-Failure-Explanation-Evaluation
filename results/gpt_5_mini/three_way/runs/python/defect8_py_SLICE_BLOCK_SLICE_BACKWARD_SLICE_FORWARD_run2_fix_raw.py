@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # language must be two lower-case letters
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        # For any longer form, position 2 must be '_'
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Now handle _CC or _CC_variant
        if length == 3 or length == 4:
            # too short to contain a two-letter country
            raise ValueError(f"Invalid locale format: {locale_str}")
        # country must be two upper-case letters at positions 3 and 4
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        # length >= 6: must have '_' at position 5 to start variant
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # variant may be empty or any value after position 6
        variant = locale_str[6:]
        return Locale(locale_str[0:2], locale_str[3:5], variant)
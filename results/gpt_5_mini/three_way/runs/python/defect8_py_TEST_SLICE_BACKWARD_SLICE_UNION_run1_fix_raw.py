@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length == 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        # For other lengths, must be at least 5 for language + '_' + country or 4 for language + '__' + variant minimal
        if length < 4:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Validate language
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Separator after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Handle language__variant (empty country)
        if length >= 4 and locale_str[3] == '_':
            # variant starts at index 4, can be empty? must be at least one char to be valid
            if length == 4:
                # nothing after second underscore
                return Locale(locale_str[0:2], "", "")
            # variant is the rest
            return Locale(locale_str[0:2], "", locale_str[4:])
        # Otherwise expect country at positions 3 and 4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        # length >= 7 expected for variant (with underscore at pos 5)
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 6:
            # nothing after underscore
            return Locale(locale_str[0:2], locale_str[3:5], "")
        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
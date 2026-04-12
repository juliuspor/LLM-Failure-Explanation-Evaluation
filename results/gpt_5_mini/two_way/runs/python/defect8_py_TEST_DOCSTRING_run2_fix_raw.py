@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1] if length > 1 else ''
        if not ('a' <= ch0 <= 'z') or not ('a' <= ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(locale_str, "")
        # length >= 3
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # Now handle possible forms:
        # lang__variant (empty country)
        if length >= 4 and locale_str[3] == '_':
            # variant must be non-empty
            variant = locale_str[4:]
            if not variant:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", variant)
        # Otherwise expect country at positions 3-4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('A' <= ch3 <= 'Z') or not ('A' <= ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        # length > 5: expect '_' at position 5 then variant
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if not variant:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], variant)
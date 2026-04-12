@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # Minimum length is 2 for language
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # language must be two lowercase letters
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch0 = locale_str[0]
        ch1 = locale_str[1] if length > 1 else ''
        if not (ch0 >= 'a' and ch0 <= 'z' and ch1 >= 'a' and ch1 <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Only language
        if length == 2:
            return Locale(locale_str, "")

        # If more, next char must be '_' to denote country or empty country
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Handle cases like 'll_' (invalid) or 'll_CC' or 'll__VAR'
        # If next is '_' then country is empty and variant starts at pos 3
        if length >= 4 and locale_str[3] == '_':
            # variant must exist after second underscore
            if length == 4:
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[4:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", variant)

        # Otherwise expect country of 2 uppercase letters starting at pos 3
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not (ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Exactly language and country
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])

        # More characters: must have '_' then variant
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5], variant)
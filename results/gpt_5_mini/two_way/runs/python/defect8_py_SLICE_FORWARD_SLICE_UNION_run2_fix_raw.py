@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)

    # language must be exactly 2 lowercase letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    if not (locale_str[0].islower() and locale_str[0].isalpha() and
            locale_str[1].islower() and locale_str[1].isalpha()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Simple language only: "xx"
    if length == 2:
        return Locale(locale_str[0:2], "")

    # Next character must be underscore
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language + country: "xx_YY" (length == 5)
    if length == 5:
        # validate country two uppercase letters
        if not (locale_str[3].isupper() and locale_str[3].isalpha() and
                locale_str[4].isupper() and locale_str[4].isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], locale_str[3:5])

    # language + country + variant: must have underscore before variant at index 5
    if length > 5:
        # need at least underscore at position 5 and a non-empty variant after
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 6:
            # empty variant
            raise ValueError(f"Invalid locale format: {locale_str}")
        # validate country two uppercase letters at positions 3 and 4
        if not (locale_str[3].isupper() and locale_str[3].isalpha() and
                locale_str[4].isupper() and locale_str[4].isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        return Locale(locale_str[0:2], locale_str[3:5], variant)

    # Fallback
    raise ValueError(f"Invalid locale format: {locale_str}")
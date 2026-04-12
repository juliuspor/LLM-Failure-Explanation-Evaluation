@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Minimum is 2 (language)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language (two lower-case letters)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1] if length > 1 else ''
    if not (ch0 >= 'a' and ch0 <= 'z' and ch1 >= 'a' and ch1 <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If only language
    if length == 2:
        return Locale(locale_str[0:2], "")

    # Must have separator at position 2
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now handle possible forms:
    # lang__variant  -> underscore at 2 and 3 (empty country)
    # lang_CC        -> length == 5 and positions 3,4 are uppercase letters
    # lang_CC_variant -> underscore at 5, variant from 6 onwards
    # Validate that there is something after the separators when variant expected

    # Empty country, variant present (lang__variant)
    if length >= 4 and locale_str[3] == '_':
        # Variant must exist after the second underscore
        if length == 4:
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[4:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], "", variant)

    # Country is expected in positions 3 and 4
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not (ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # lang_CC
    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # lang_CC_variant -> must have '_' at position 5 and variant after
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    variant = locale_str[6:]
    if len(variant) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(locale_str[0:2], locale_str[3:5], variant)
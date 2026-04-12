@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language must be two lower-case letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # simple language only
    if length == 2:
        return Locale(locale_str, "")

    # must have separator after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now handle cases like: xx__variant (empty country), xx_YY, xx_YY_variant
    # If next char is '_' then country is empty and variant follows
    if length >= 4 and locale_str[3] == '_':
        # format: xx__variant -> country is empty, variant starts at pos 4
        if length == 4:
            # nothing after second underscore
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[4:]
        return Locale(locale_str[0:2], "", variant)

    # Otherwise expect two-letter country at positions 3 and 4
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # country only
    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # must have second separator before variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # variant may be empty? treat empty variant as empty string
    variant = locale_str[6:] if length > 6 else ""
    return Locale(locale_str[0:2], locale_str[3:5], variant)

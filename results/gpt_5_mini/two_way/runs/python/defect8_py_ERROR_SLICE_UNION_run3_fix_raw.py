@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Must be at least 2 chars for language
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language: first two chars must be lowercase letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # just language
    if length == 2:
        return Locale(locale_str[0:2], "")

    # Next must be an underscore
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If length == 3, that's invalid (e.g. 'en_')
    if length == 3:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Cases:
    # ll_CC (length == 5)
    # ll__VVVV (third char '_' and fourth char '_' -> empty country, variant starts at index 3?)
    # ll_CC_VVVV (with variant)

    # If there's another underscore at position 3, it's an empty country and variant follows at pos 3+1
    if locale_str[3] == '_':
        # variant must exist after the second underscore
        if length <= 4:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # variant is rest after the second underscore
        return Locale(locale_str[0:2], "", locale_str[4:])

    # Otherwise, expect two uppercase letters for country at positions 3 and 4
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # ll_CC
    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])

    # ll_CC_VVVV -> next must be underscore
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    if length <= 6:
        raise ValueError(f"Invalid locale format: {locale_str}")
    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
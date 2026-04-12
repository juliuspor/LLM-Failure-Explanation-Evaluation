@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language must be two lowercase letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")

    # must have '_' after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now handle country and variant. Possible forms:
    # ll_CC, ll__VVV, ll_CC_VVV
    # Check if country is empty (i.e., second underscore at pos 3)
    if length < 4:
        # forms like "a_" or too short
        raise ValueError(f"Invalid locale format: {locale_str}")

    if locale_str[3] == '_':
        # empty country, variant starts at index 4
        country = ""
        if length == 4:
            # string ends with two underscores and no variant
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[4:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], country, variant)
    else:
        # country should be two uppercase letters at pos 3 and 4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[3:5]
        if length == 5:
            return Locale(locale_str[0:2], country)
        # if there's more, position 5 must be '_'
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], country, variant)
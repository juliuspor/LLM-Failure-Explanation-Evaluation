@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language (first two chars must be lowercase letters)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")

    # Must have an underscore after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # If nothing after "xx_" -> invalid
    if length == 3:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Find next underscore after position 2
    next_underscore = locale_str.find('_', 3)
    if next_underscore == -1:
        # No second underscore: the rest is country
        country = locale_str[3:]
        # country must be exactly 2 uppercase letters
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], country)
    else:
        # There is a variant part. Country is between pos 3 and next_underscore (may be empty)
        country = locale_str[3:next_underscore]
        variant = locale_str[next_underscore+1:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(country) == 0:
            # empty country allowed, return language and variant
            return Locale(locale_str[0:2], "", variant)
        # non-empty country must be exactly 2 uppercase letters
        if len(country) != 2 or not country.isupper() or not country.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], country, variant)
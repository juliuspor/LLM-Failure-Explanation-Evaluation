@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # Accept: 2 (language), 5 (language_COUNTRY), >=4 for language__variant or language_COUNTRY_variant
    if length != 2 and length != 5 and length < 4:
        raise ValueError(f"Invalid locale format: {locale_str}")

    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")
    else:
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Handle empty country (double underscore) form: language__variant
        if length >= 4 and locale_str[3] == '_':
            # Variant must exist after the second underscore
            if length == 4:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", locale_str[4:])

        # Otherwise expect two uppercase letters for country at positions 3 and 4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")

        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 6:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
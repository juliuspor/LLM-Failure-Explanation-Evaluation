@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Accept Java-style underscores and also the form language@variant
    # Normalize and parse
    # Quick length checks: language (2) or language_country (5) or language__variant or language_country_variant
    length = len(locale_str)

    # Validate basic language letters
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1] if length > 1 else ''
    if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Handle forms with '@' variant, e.g. 'fr@POSIX'
    if '@' in locale_str:
        parts = locale_str.split('@', 1)
        base = parts[0]
        variant = parts[1]
        if len(base) == 2:
            # language@variant
            return Locale(base, "", variant)
        elif len(base) == 5 and base[2] == '_' and 'A' <= base[3] <= 'Z' and 'A' <= base[4] <= 'Z':
            return Locale(base[0:2], base[3:5], variant)
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")

    # Handle underscore forms
    # language only
    if length == 2:
        return Locale(locale_str, "")

    # must have at least language + '_' + something
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # After first underscore: could be country (2 uppercase), empty country (i.e. another underscore), or country+variant
    # Cases:
    #  - fr__POSIX -> language, empty country, variant
    #  - fr_POSIX  -> ambiguous: treat as language + variant (country empty)
    #  - fr_FR     -> language + country
    #  - fr_FR_POSIX -> language + country + variant

    # If double underscore -> empty country, variant follows
    if length >= 4 and locale_str[3] == '_':
        # double underscore, variant starts at pos 4
        variant = locale_str[4:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str[0:2], "", variant)

    # Otherwise, check for two-letter country
    if length >= 5:
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
            # treat as language + variant with underscore, e.g. fr_POSIX -> language, variant
            variant = locale_str[3:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], "", variant)

        # Valid country present
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            # Expect '_' before variant
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:]
            return Locale(locale_str[0:2], locale_str[3:5], variant)
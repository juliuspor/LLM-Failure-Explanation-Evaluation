@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # minimal valid lengths: 2 (language), 5 (language_country), >=7 (language_country_variant)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # language must be two ASCII letters
    if length >= 2:
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if not (ch0.isalpha() and ch1.isalpha() and ch0.islower() and ch1.islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")

    # Expect a separator at position 2
    sep1 = locale_str[2]
    if sep1 not in ('_', '-'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Ensure we have at least two characters for country at positions 3 and 4
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")

    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not (ch3.isalpha() and ch4.isalpha()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Construct country as uppercase
    country = (ch3 + ch4).upper()

    if length == 5:
        return Locale(locale_str[0:2], country)

    # Expect a separator at position 5 for variant
    sep2 = locale_str[5]
    if sep2 not in ('_', '-'):
        raise ValueError(f"Invalid locale format: {locale_str}")

    variant = locale_str[6:]
    if variant == "":
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(locale_str[0:2], country, variant)
@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    # valid lengths: 2 (language), 5 (language_country), >=7 (language_country_variant)
    if length == 2:
        # validate language
        if not (locale_str[0].islower() and locale_str[1].islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(locale_str, "")

    # For longer forms, ensure the separator at position 2 is '_'
    if length < 5 or locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Now safe to access positions 3 and 4 for country
    country_part = locale_str[3:5]
    if len(country_part) != 2 or not (country_part[0].isupper() and country_part[1].isupper()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 5:
        return Locale(locale_str[0:2], country_part)

    # length >= 7 for variant form; ensure separator at position 5 is '_'
    if locale_str[5] != '_' or length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")

    variant_part = locale_str[6:]
    if len(variant_part) == 0:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # validate language part
    lang_part = locale_str[0:2]
    if not (lang_part[0].islower() and lang_part[1].islower()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    return Locale(lang_part, country_part, variant_part)
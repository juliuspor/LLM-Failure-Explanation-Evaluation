@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    """
    Parse a locale string into a `Locale` object.

    This translation follows the underscore-separated forms used by the
    Java implementation and validates casing and separators.

    Examples:
        LocaleUtils.to_locale("en")        -> Locale("en", "")
        LocaleUtils.to_locale("en_GB")     -> Locale("en", "GB")
        LocaleUtils.to_locale("en_GB_xxx") -> Locale("en", "GB", "xxx")

    Args:
        locale_str: Locale string to convert. If None, returns None.
        
    Returns:
        A `Locale` instance, or None if `locale_str` is None.
        
    Raises:
        ValueError: If `locale_str` does not match the expected format.
    """
    if locale_str is None:
        return None
    
    parts = locale_str.split('_', 2)
    if len(parts) == 1:
        language = parts[0]
        if len(language) != 2 or not (language[0].islower() and language[1].islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, "", "")
    elif len(parts) == 2:
        language = parts[0]
        country_or_variant = parts[1]
        if len(language) != 2 or not (language[0].islower() and language[1].islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(country_or_variant) == 2 and country_or_variant.isupper():
            return Locale(language, country_or_variant, "")
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")
    elif len(parts) == 3:
        language = parts[0]
        country = parts[1]
        variant = parts[2]
        if (len(language) != 2 or not (language[0].islower() and language[1].islower()) or
            not (country.isupper() and len(country) in (0, 2)) or
            len(variant) == 0):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)
    else:
        raise ValueError(f"Invalid locale format: {locale_str}")
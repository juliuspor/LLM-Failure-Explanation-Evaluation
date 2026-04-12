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
        LocaleUtils.to_locale("fr__POSIX") -> Locale("fr", "", "POSIX")

    Args:
        locale_str: Locale string to convert. If None, returns None.
        
    Returns:
        A `Locale` instance, or None if `locale_str` is None.
        
    Raises:
        ValueError: If `locale_str` does not match the expected format.
    """
    if locale_str is None:
        return None
    
    parts = locale_str.split('_')
    if len(parts) < 1 or len(parts) > 3:
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    language = parts[0]
    if len(language) != 2 or not (language[0].islower() and language[1].islower()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    country = ""
    variant = ""
    
    if len(parts) >= 2:
        country_part = parts[1]
        if len(country_part) == 2 and country_part.isupper():
            country = country_part
        elif len(country_part) != 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
    if len(parts) == 3:
        variant = parts[2]
    elif len(parts) == 2 and len(parts[1]) == 0:
        # Handle language__variant case
        if len(parts) == 2:
            variant = parts[1]
            country = ""
    
    return Locale(language, country, variant)
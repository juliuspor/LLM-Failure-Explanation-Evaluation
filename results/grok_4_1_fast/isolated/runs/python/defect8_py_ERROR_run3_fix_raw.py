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
    
    parts = locale_str.split('_')
    if len(parts) < 1 or len(parts) > 3:
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    language = parts[0]
    if len(language) != 2 or not (language[0].islower() and language[1].islower()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    country = ""
    variant = ""
    
    if len(parts) >= 2:
        country_candidate = parts[1]
        if len(country_candidate) == 2 and country_candidate.isupper():
            country = country_candidate
        else:
            variant = '_'.join(parts[1:])
            if not variant:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "", variant)
    
    if len(parts) == 3:
        variant_candidate = parts[2]
        if not variant_candidate:
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = variant_candidate
    
    return Locale(language, country, variant)
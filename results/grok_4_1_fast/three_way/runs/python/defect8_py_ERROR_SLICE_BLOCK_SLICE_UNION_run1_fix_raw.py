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
    
    length = len(locale_str)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    # Validate language: positions 0-1 must be lowercase letters
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    language = locale_str[0:2]
    
    if length == 2:
        return Locale(language, "")
    
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    if length == 5:
        # language_country format: xx_YY
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[3:5]
        return Locale(language, country)
    
    if length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    # language_country_variant format: xx_YY_zzzz
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    country = locale_str[3:5]
    variant = locale_str[6:]
    return Locale(language, country, variant)
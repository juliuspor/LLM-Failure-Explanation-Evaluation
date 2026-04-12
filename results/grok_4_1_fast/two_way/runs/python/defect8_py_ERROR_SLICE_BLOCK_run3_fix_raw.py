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
    
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    if length == 2:
        return Locale(locale_str, "")
    
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    # Find country code - skip extra underscores
    country_start = 3
    while country_start < length and locale_str[country_start] == '_':
        country_start += 1
    
    if country_start + 1 >= length:
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    ch3 = locale_str[country_start]
    ch4 = locale_str[country_start + 1]
    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    country_end = country_start + 2
    
    # Find variant
    variant_start = country_end
    while variant_start < length and locale_str[variant_start] == '_':
        variant_start += 1
    
    if variant_start == length:
        # No variant
        return Locale(locale_str[0:2], locale_str[country_start:country_end])
    else:
        return Locale(locale_str[0:2], locale_str[country_start:country_end], locale_str[variant_start:])

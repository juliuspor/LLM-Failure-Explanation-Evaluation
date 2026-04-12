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
    else:
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Find country end (next underscore or end of string)
        country_start = 3
        country_end = locale_str.find('_', country_start)
        if country_end == -1:
            country_end = length
        
        country = locale_str[country_start:country_end]
        
        # Validate country (allow empty)
        if len(country) > 0 and (country[0] < 'A' or country[0] > 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if country_end == length:
            # No variant
            return Locale(locale_str[0:2], country)
        else:
            # Has variant
            variant = locale_str[country_end + 1:]
            return Locale(locale_str[0:2], country, variant)
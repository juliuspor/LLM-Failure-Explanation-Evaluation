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
    if length != 2 and length != 5 and length < 7:
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
        
        # Find first non-empty part after language
        country_start = 3
        while country_start < length and locale_str[country_start] == '_':
            country_start += 1
        
        if country_start == length:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country_end = country_start
        while country_end < length and locale_str[country_end] != '_':
            country_end += 1
        
        country = locale_str[country_start:country_end]
        
        ch_country = country[0] if country else ''
        if country and (ch_country < 'A' or ch_country > 'Z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if country_end == length:
            return Locale(locale_str[0:2], country)
        elif locale_str[country_end] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        else:
            variant = locale_str[country_end + 1:]
            return Locale(locale_str[0:2], country, variant)
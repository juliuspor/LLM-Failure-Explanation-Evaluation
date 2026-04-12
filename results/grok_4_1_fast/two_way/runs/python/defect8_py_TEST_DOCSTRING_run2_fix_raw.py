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
    
    # Validate language (positions 0-1)
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    language = locale_str[0:2]
    
    if length == 2:
        return Locale(language, "")
    
    # Check for separator after language
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    # Find variant separator (second '_')
    variant_pos = locale_str.find('_', 3)
    
    if variant_pos == -1:
        # No variant, just country
        country = locale_str[3:]
        if len(country) != 2 or not all('A' <= c <= 'Z' for c in country):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country)
    else:
        # Has variant
        country_start = 3
        country_end = variant_pos
        
        if country_end == country_start:
            # Empty country: fr__POSIX
            country = ""
            variant = locale_str[country_end + 1:]
        else:
            # Has country: en_GB_POSIX
            country = locale_str[country_start:country_end]
            if len(country) != 2 or not all('A' <= c <= 'Z' for c in country):
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[country_end + 1:]
        
        return Locale(language, country, variant)

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
        # Skip all underscores after language
        country_start = 2
        while country_start < length and locale_str[country_start] == '_':
            country_start += 1
        
        if country_start == length or country_start == 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Find variant separator (next underscores)
        variant_start = country_start
        while variant_start < length and locale_str[variant_start] != '_':
            variant_start += 1
        
        country_end = variant_start
        
        # Validate country part (2 uppercase letters)
        if country_end - country_start != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        ch3 = locale_str[country_start]
        ch4 = locale_str[country_start + 1]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = locale_str[0:2]
        country = locale_str[country_start:country_start+2]
        
        if variant_start < length:
            # Skip underscores before variant
            var_start = variant_start + 1
            while var_start < length and locale_str[var_start] == '_':
                var_start += 1
            variant = locale_str[var_start:]
            if not variant:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
        else:
            return Locale(language, country)
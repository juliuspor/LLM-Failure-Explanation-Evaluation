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
        
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        
        if length == 5:
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            # For length >= 7, check if it's language_country_variant or language__variant
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            # Check if positions 3:5 form valid country code
            if ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z':
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
            else:
                # Empty country case: language__variant
                return Locale(locale_str[0:2], "", locale_str[4:])
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
    if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    if length == 2:
        return Locale(locale_str, "")
    
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    # Check country code (positions 3-4)
    if length < 5:
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    if length == 5:
        return Locale(locale_str[0:2], locale_str[3:5])
    
    # Check second underscore for variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])

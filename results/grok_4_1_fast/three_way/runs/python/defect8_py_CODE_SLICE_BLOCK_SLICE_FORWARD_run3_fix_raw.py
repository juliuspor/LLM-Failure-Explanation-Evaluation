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
    if not ((2 <= length <= 5) or length >= 7):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    # Validate language (lowercase letters)
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if not ('a' <= ch0 <= 'z' and 'a' <= ch1 <= 'z'):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    language = locale_str[0:2]
    
    if length == 2:
        return Locale(language, "")
    
    # Check first separator
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    # Validate country (uppercase letters)
    ch3 = locale_str[3]
    ch4 = locale_str[4]
    if not ('A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z'):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    country = locale_str[3:5]
    
    if length == 5:
        return Locale(language, country)
    
    # Check second separator for variant
    if locale_str[5] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    # Validate variant (alphanumeric + underscore)
    variant = locale_str[6:]
    for ch in variant:
        if not (('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ('0' <= ch <= '9') or ch == '_'):
            raise ValueError(f"Invalid locale format: {locale_str}")
    
    return Locale(language, country, variant)
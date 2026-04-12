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
    
    if len(locale_str) < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    # Validate language: exactly 2 lowercase letters
    if not (locale_str[0].islower() and locale_str[1].islower()):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    language = locale_str[0:2]
    pos = 2
    
    country = ""
    variant = ""
    
    if pos < len(locale_str) and locale_str[pos] == '_':
        pos += 1
        # Country must be exactly 2 uppercase letters
        if pos + 1 >= len(locale_str) or not (locale_str[pos].isupper() and locale_str[pos+1].isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[pos:pos+2]
        pos += 2
        
        # Optional variant
        if pos < len(locale_str):
            if locale_str[pos] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            pos += 1
            variant = locale_str[pos:]
    
    if pos != len(locale_str):
        raise ValueError(f"Invalid locale format: {locale_str}")
    
    return Locale(language, country, variant)

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
        
        # Validate first two characters are lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 2, it's just language
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least 3 characters for separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, that's just language + underscore (invalid)
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check if we have a double underscore (empty country)
        if length >= 4 and locale_str[3] == '_':
            # Format: language__variant
            # Language is first two chars, country empty, variant after double underscore
            if length == 4:
                # Only double underscore, no variant (invalid)
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[4:]
            return Locale(locale_str[0:2], "", variant)
        
        # Otherwise, we have at least country code (two uppercase letters)
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 5, it's language_country
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        
        # Must have separator after country
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 6, that's just language_country_ (invalid)
        if length == 6:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # language_country_variant
        variant = locale_str[6:]
        return Locale(locale_str[0:2], locale_str[3:5], variant)
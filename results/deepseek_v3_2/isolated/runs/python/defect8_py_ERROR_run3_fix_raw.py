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
        
        # Handle special POSIX locale
        if locale_str.upper() in ('C', 'POSIX'):
            return Locale('', '')
        
        # Handle locale strings with encoding (e.g., 'fr_FR.UTF-8')
        # Split on '.' to remove encoding part
        if '.' in locale_str:
            locale_str = locale_str.split('.')[0]
        
        length = len(locale_str)
        if length == 0:
            return Locale('', '')
        
        # Check for language only (2 or 3 chars)
        if '_' not in locale_str:
            # Language code must be all letters
            if not locale_str.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str.lower(), "")
        
        # Split by underscore
        parts = locale_str.split('_')
        if len(parts) < 2 or len(parts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        country = parts[1] if len(parts) >= 2 else ""
        variant = parts[2] if len(parts) == 3 else ""
        
        # Validate language (ISO 639 alpha-2 or alpha-3)
        if not language.isalpha() or len(language) < 2 or len(language) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate country (ISO 3166 alpha-2 or UN M.49 numeric-3)
        if country:
            if not (country.isalpha() and len(country) == 2) and not country.isdigit():
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Variant can be any string
        return Locale(language.lower(), country.upper(), variant)

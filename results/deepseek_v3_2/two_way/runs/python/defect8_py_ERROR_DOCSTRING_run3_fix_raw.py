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
        
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0].lower()
        if len(language) != 2 or not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            country_part = parts[1]
            if country_part:
                if len(country_part) != 2 or not country_part.isalpha():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = country_part.upper()
            
            if len(parts) >= 3:
                variant = '_'.join(parts[2:])  # Join remaining parts with '_' in case variant contains underscores
        
        return Locale(language, country, variant)
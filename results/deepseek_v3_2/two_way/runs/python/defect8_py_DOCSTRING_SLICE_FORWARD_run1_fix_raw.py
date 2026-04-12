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
        
        parts = locale_str.split('_', 2)  # maxsplit=2: language, country, variant
        language = parts[0]
        country = ""
        variant = ""
        
        if len(parts) > 1:
            country = parts[1]
        if len(parts) > 2:
            variant = parts[2]
        
        # Validate language
        if not language:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not (2 <= len(language) <= 3 and language.isalpha() and language.islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate country if present
        if country:
            if len(country) == 2:
                if not country.isalpha() or not country.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
            elif len(country) == 3:
                # UN M.49 numeric-3 area code: three digits
                if not country.isdigit():
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Variant can be any string, no validation needed
        
        return Locale(language, country, variant)
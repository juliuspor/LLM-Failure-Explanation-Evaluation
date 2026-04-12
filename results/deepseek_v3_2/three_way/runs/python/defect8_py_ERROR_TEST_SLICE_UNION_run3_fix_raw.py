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
        
        # Handle empty string
        if not locale_str:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Split by underscore
        parts = locale_str.split('_')
        
        # Validate at least one part (language) exists
        if not parts or not parts[0]:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        country = ""
        variant = ""
        
        # Validate language: must be two letters, all lowercase
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if len(parts) > 1:
            # Check if second part is a country code (two uppercase letters)
            if len(parts[1]) == 2 and parts[1].isalpha() and parts[1].isupper():
                country = parts[1]
                # If there are more parts, the rest is variant (joined by underscore)
                if len(parts) > 2:
                    variant = '_'.join(parts[2:])
            else:
                # Second part is not a country code, treat as variant (country empty)
                # This handles the double underscore case: language__variant
                variant = '_'.join(parts[1:])
                country = ""
        
        return Locale(language, country, variant)
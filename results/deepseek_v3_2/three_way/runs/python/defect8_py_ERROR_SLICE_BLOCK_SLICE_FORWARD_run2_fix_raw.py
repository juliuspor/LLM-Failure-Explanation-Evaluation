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
        
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # First part must be language code (2 or 3 letters, lowercase)
        language = parts[0]
        if not language:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Initialize country and variant
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            second = parts[1]
            if second:
                # Second part could be country or variant if empty country
                # According to Java Locale, country must be uppercase letters or digits
                # But we also allow empty string for country (double underscore)
                if second.isupper() and len(second) == 2:
                    # Assume it's a country code
                    country = second
                else:
                    # Treat as variant, and country remains empty
                    variant = second
            
            # If there are more parts, they are part of variant
            if len(parts) >= 3:
                # Join remaining parts with underscore as variant
                variant_parts = parts[2:]
                if variant:
                    # If we already set variant from second part, prepend it
                    variant_parts.insert(0, variant)
                variant = '_'.join(variant_parts)
        
        return Locale(language, country, variant)
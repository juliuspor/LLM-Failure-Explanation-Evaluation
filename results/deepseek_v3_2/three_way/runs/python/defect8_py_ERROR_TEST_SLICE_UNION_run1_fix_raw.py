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
        # Check for language only (2 or 3 chars) and language with country/variant
        # The original check was too restrictive; we need to allow language codes of length 2 or 3.
        # Also, we need to handle the double underscore case (language__variant).
        # We'll first validate the language part.
        # Find the first underscore.
        underscore1 = locale_str.find('_')
        if underscore1 == -1:
            # No underscore: language only
            # Language must be at least 2 chars, but could be 2 or 3 (ISO 639).
            if length < 2:
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Validate language code: all lowercase letters
            for ch in locale_str:
                if ch < 'a' or ch > 'z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        else:
            # There is at least one underscore.
            language = locale_str[:underscore1]
            if len(language) < 2:
                raise ValueError(f"Invalid locale format: {locale_str}")
            for ch in language:
                if ch < 'a' or ch > 'z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
            
            # Check for double underscore (language__variant)
            if underscore1 + 1 < length and locale_str[underscore1 + 1] == '_':
                # Double underscore: country is empty, variant starts after second underscore
                variant_start = underscore1 + 2
                if variant_start >= length:
                    # No variant after double underscore? That's invalid.
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[variant_start:]
                # Variant can be any string, but we should ensure it's not empty.
                if not variant:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(language, "", variant)
            else:
                # Single underscore: could be language_country or language_country_variant
                # Extract country (next two chars after underscore)
                if underscore1 + 2 > length:
                    # Not enough for country code
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = locale_str[underscore1 + 1:underscore1 + 3]
                # Validate country code: two uppercase letters
                if len(country) != 2 or country[0] < 'A' or country[0] > 'Z' or country[1] < 'A' or country[1] > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                
                # Check if there is a variant after another underscore
                if underscore1 + 3 < length and locale_str[underscore1 + 3] == '_':
                    # There is a variant
                    variant_start = underscore1 + 4
                    if variant_start >= length:
                        # No variant after third underscore? That's invalid.
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    variant = locale_str[variant_start:]
                    return Locale(language, country, variant)
                else:
                    # No variant, just language and country
                    if underscore1 + 3 != length:
                        # There are extra characters after country without underscore
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(language, country, "")

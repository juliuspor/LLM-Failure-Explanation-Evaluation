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
        
        # Handle empty string case
        if not locale_str:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Split by underscore
        parts = locale_str.split('_')
        if len(parts) == 0 or len(parts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if not language:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate language code: must be 2 or 3 letters, all lowercase
        if not (2 <= len(language) <= 3 and language.isalpha() and language.islower()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            country = parts[1]
            if country:
                # Country code must be 2 letters or 3 digits, uppercase if letters
                if len(country) == 2 and country.isalpha():
                    country = country.upper()
                elif len(country) == 3 and country.isdigit():
                    # UN M.49 numeric-3 area code, keep as is
                    pass
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
            # If country part is empty, it's allowed (e.g., "en__variant")
        
        if len(parts) == 3:
            variant = parts[2]
            # Variant can be any non-empty string
            if not variant:
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        return Locale(language, country, variant)
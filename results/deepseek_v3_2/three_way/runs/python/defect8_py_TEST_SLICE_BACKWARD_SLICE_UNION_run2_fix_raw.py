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
        if len(parts) == 1:
            # Only language
            lang = parts[0]
            if len(lang) != 2 and len(lang) != 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, "")
        elif len(parts) == 2:
            # language and country, or language and variant (if country empty)
            lang = parts[0]
            second = parts[1]
            if len(lang) != 2 and len(lang) != 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Check if second part is a country (2 letters) or variant
            if len(second) == 2 and second.isalpha() and second.isupper():
                # Treat as country
                return Locale(lang, second)
            else:
                # Treat as variant, country empty
                return Locale(lang, "", second)
        elif len(parts) == 3:
            # language, country, variant
            lang, country, variant = parts
            if len(lang) != 2 and len(lang) != 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country, variant)
        else:
            # More than 3 parts? Not standard, but we can treat extra parts as part of variant
            # However, the original Java Locale only allows three parts.
            # We'll follow the original strictness.
            raise ValueError(f"Invalid locale format: {locale_str}")
    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        """
        Parse a locale string into a Locale.

        This translation follows the underscore-separated forms used by the
        JDK, but is more flexible: it allows empty country codes (two underscores
        before variant) and variant can contain underscores.

        Examples:
            LocaleUtils.to_locale("en")         -> Locale("en", "")
            LocaleUtils.to_locale("en_GB")      -> Locale("en", "GB")
            LocaleUtils.to_locale("en_GB_xxx")  -> Locale("en", "GB", "xxx")
            LocaleUtils.to_locale("fr__POSIX")  -> Locale("fr", "", "POSIX")
            LocaleUtils.to_locale("fr__POSIX_EXT") -> Locale("fr", "", "POSIX_EXT")

        Args:
            locale_str: Locale string to convert. If None, returns None.

        Returns:
            A Locale, or None if locale_str is None.

        Raises:
            ValueError: If locale_str does not follow the expected pattern.
        """
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if not language.isalpha() or len(language) < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            # The second part could be a country code or the start of a variant
            if len(parts[1]) == 2 and parts[1].isalpha() and parts[1].isupper():
                country = parts[1]
                if len(parts) >= 3:
                    variant = '_'.join(parts[2:])
            else:
                # No country, second part is variant
                variant = '_'.join(parts[1:])
        
        return Locale(language, country, variant)
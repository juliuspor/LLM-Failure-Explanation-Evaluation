    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        """
        Parse a locale string into a `Locale` object.

        This translation follows the underscore-separated forms used by the
        Java implementation and validates casing and separators.

        Examples:
            LocaleUtils.to_locale("en")        -> Locale("en", "")
            LocaleUtils.to_locale("eng")       -> Locale("eng", "")
            LocaleUtils.to_locale("en_GB")     -> Locale("en", "GB")
            LocaleUtils.to_locale("eng_GB")    -> Locale("eng", "GB")
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
        if length == 2 or length == 3:
            # language only
            if not locale_str.isalpha() or not locale_str.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        elif length == 5 or length == 6:
            # language_country
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            lang = locale_str[0:2]
            country = locale_str[3:5]
            if not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country)
        elif length >= 8:
            # language_country_variant
            if locale_str[2] != '_' or locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            lang = locale_str[0:2]
            country = locale_str[3:5]
            variant = locale_str[6:]
            if not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country, variant)
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")
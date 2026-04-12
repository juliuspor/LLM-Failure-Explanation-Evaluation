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
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate first two characters are lowercase letters
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least 3 characters to include separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore (e.g., "en_") - treat as language only
            return Locale(locale_str[0:2], "")
        
        # Now length >= 4
        # Check if there's a country code (two uppercase letters) after underscore
        if length >= 5 and locale_str[3].isupper() and locale_str[4].isupper():
            # We have a country code at positions 3 and 4
            country = locale_str[3:5]
            if length == 5:
                return Locale(locale_str[0:2], country)
            else:
                # Must have another underscore before variant
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], country, variant)
        else:
            # No country code, variant directly after underscore
            # Example: "fr_POSIX" (single underscore) or "fr__POSIX" (double underscore)
            # We need to handle both: if there is a double underscore, treat the second underscore as part of variant?
            # Actually, the standard format is language + underscore + variant (no country).
            # But the variant may contain underscores. However, the Java Locale constructor
            # expects variant to be the part after the second underscore (if country present) or after first underscore (if no country).
            # In the case of "fr__POSIX", the string has two underscores before variant.
            # We should treat the first underscore as separator, and the second underscore as part of variant?
            # However, the typical POSIX locale is "fr_POSIX" (single underscore).
            # To be compatible with Java's Locale.forLanguageTag, we should parse as:
            # If after the first underscore, the next two characters are not both uppercase letters,
            # then there is no country code, and the rest (including any additional underscores) is the variant.
            # So we take everything after the first underscore as variant.
            variant = locale_str[3:] if length > 3 else ""
            return Locale(locale_str[0:2], "", variant)
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
        
        # If length is 2, it's just language
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least 3 characters to have a separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, that's just language + underscore (invalid)
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: xx_?
        # Check if the next part is a country (two uppercase letters) or empty country (another underscore)
        if length >= 5 and locale_str[3] != '_':
            # Possibly a country code
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # We have a valid country code
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # Must have underscore after country
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # Return with variant
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
        else:
            # The character at position 3 is '_' (empty country) or length is 4 (only one char after first underscore)
            # If length is 4, that's xx_? where ? is not underscore (since we already checked length >=5 for country)
            # Actually, if length is 4, then locale_str[3] is the only character after underscore.
            # According to Java's Locale, empty country with variant is represented as xx__variant (double underscore).
            # So if length >=4 and locale_str[3] == '_', then we have empty country and possibly variant.
            if length >= 4 and locale_str[3] == '_':
                # Empty country, variant may start after second underscore
                if length == 4:
                    # Just xx__ (double underscore with nothing after) - treat as empty variant?
                    # Java's Locale.forLanguageTag would treat as empty variant? Actually, "fr__" is invalid.
                    # We'll treat as language only? But there is an extra underscore. Safer to raise error.
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # There is at least one character after the second underscore
                # The variant starts at position 4? Wait: indices: 0,1,2,3,4...
                # locale_str[2] is first '_', locale_str[3] is second '_', variant starts at index 4.
                # However, we need to ensure there is at least one character after the second underscore.
                # Actually, if length >=5, we already know locale_str[3] == '_', so variant starts at index 4.
                # But we also need to check that there is no third underscore? Not necessary.
                # Return with empty country and variant.
                return Locale(locale_str[0:2], "", locale_str[4:])
            else:
                # length is 4 and locale_str[3] != '_' (i.e., a single character after underscore)
                # This is invalid because country codes must be two letters.
                raise ValueError(f"Invalid locale format: {locale_str}")
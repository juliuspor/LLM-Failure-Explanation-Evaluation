    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
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
        
        # Must have at least 3 characters to have a separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore (e.g., "en_"? but that's odd, treat as language only?)
            # According to Java Locale, this is invalid. We'll raise error.
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: xx_?
        # The part after first underscore could be country (2 uppercase) or variant (any)
        # We need to parse like Java's Locale does: language_country_variant
        # where country is optional but if present must be 2 uppercase letters,
        # variant is optional and can be any length.
        # The string is split by underscores, max 3 parts.
        parts = locale_str.split('_', 2)  # max 3 parts
        language = parts[0]
        country = ""
        variant = ""
        if len(parts) >= 2:
            second = parts[1]
            if len(second) == 2 and second.isalpha() and second.isupper():
                country = second
                if len(parts) == 3:
                    variant = parts[2]
            else:
                # second part is not a valid country code, treat as variant
                variant = second
                if len(parts) == 3:
                    variant = second + '_' + parts[2]  # combine because we split only once
        else:
            # only language part (should have been caught by length==2)
            pass
        
        return Locale(language, country, variant)
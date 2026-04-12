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
        
        # Must have at least 3 characters for separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore (e.g., "en_") - treat as language only
            return Locale(locale_str[0:2], "")
        
        # Check if there is a country code (two uppercase letters after first underscore)
        if length >= 5 and locale_str[3].isalpha() and locale_str[4].isalpha() and locale_str[3].isupper() and locale_str[4].isupper():
            # We have a country code at positions 3 and 4
            country = locale_str[3:5]
            if length == 5:
                return Locale(locale_str[0:2], country)
            else:
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], country, variant)
        else:
            # No country code (double underscore or single underscore with variant starting at position 3)
            # Check if there is a second underscore immediately after the first
            if length >= 4 and locale_str[3] == '_':
                # Double underscore, variant starts at position 4
                variant = locale_str[4:] if length > 4 else ""
                return Locale(locale_str[0:2], "", variant)
            else:
                # Single underscore, variant starts at position 3 (country is empty)
                variant = locale_str[3:] if length > 3 else ""
                return Locale(locale_str[0:2], "", variant)
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
            # Only language and underscore, e.g., "fr_"? Not standard, but we can treat as language only.
            # However, the original Java Locale.forLanguageTag would not accept this.
            # We'll treat as language with empty country.
            return Locale(locale_str[0:2], "")
        
        # Now we have at least 4 characters: "fr_X..."
        # The next part could be country (uppercase) or variant (if country is empty).
        # We need to handle the case where after underscore there is another underscore (empty country).
        # Example: "fr__POSIX" -> language="fr", country="", variant="POSIX"
        
        # Check if the character at index 3 is an underscore, indicating empty country.
        if locale_str[3] == '_':
            # Empty country, variant starts at index 4
            if length == 4:
                # Only language and two underscores, e.g., "fr__" -> treat as language with empty variant.
                return Locale(locale_str[0:2], "", "")
            # variant is everything after the second underscore
            variant = locale_str[4:]
            return Locale(locale_str[0:2], "", variant)
        
        # Otherwise, we expect a country code (two uppercase letters) starting at index 3.
        if length < 5:
            # Not enough characters for a two-letter country code.
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:] if length > 6 else ""
            return Locale(locale_str[0:2], locale_str[3:5], variant)
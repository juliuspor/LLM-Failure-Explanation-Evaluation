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
            # Only language and underscore (e.g., "en_") - treat as language only
            return Locale(locale_str[0:2], "")
        
        # Now we have at least 4 characters: "xx_" + something
        # Check if there's a country code (two uppercase letters) after the underscore
        if length >= 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if 'A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z':
                # We have a valid country code
                if length == 5:
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    # Check for variant separator
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    # Variant is everything after the second underscore
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
            else:
                # No valid country code, treat as language with variant starting at position 3
                # Example: "fr__POSIX" -> language="fr", country="", variant="_POSIX"? Actually variant should be after second underscore.
                # But the string has two underscores, so we need to handle that.
                # We'll parse by splitting on underscores.
                pass
        
        # Fallback: split by underscores and handle cases like "fr__POSIX"
        parts = locale_str.split('_')
        if len(parts) < 2:
            # Should not happen because we already checked for underscore at position 2
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # The second part could be country or variant if empty string?
        # In "fr__POSIX", parts = ['fr', '', 'POSIX']
        country = ""
        variant = ""
        if len(parts) >= 2:
            second = parts[1]
            if len(second) == 2 and second.isalpha() and second.isupper():
                country = second
                # The rest (if any) are variant parts
                if len(parts) > 2:
                    variant = '_'.join(parts[2:])
            else:
                # No country, second part might be empty or start variant
                # If second is empty, variant starts from third part
                # If second is not empty, it's the variant (and there is no country)
                if second:
                    variant = '_'.join(parts[1:])
                else:
                    variant = '_'.join(parts[2:])
        
        return Locale(language, country, variant)
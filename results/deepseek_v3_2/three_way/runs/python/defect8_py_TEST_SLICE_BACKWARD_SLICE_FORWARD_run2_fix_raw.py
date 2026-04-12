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
        
        # If length is 2, only language
        if length == 2:
            return Locale(locale_str, "")
        
        # Must have at least 3 characters and underscore at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, only language and underscore (invalid, but handle gracefully?)
        # Actually, length 3 would be like "en_" which is invalid per Java's Locale.
        # We'll treat it as language only? But spec says underscore must be followed by country.
        # Let's follow the original logic: if length == 3, it's invalid because country missing.
        # However, we need to support double underscore for empty country.
        # So we need to check if the next character after the first underscore is another underscore.
        # If so, then country is empty and variant starts after the double underscore.
        if length == 3:
            # Only language and underscore, e.g., "en_" -> invalid
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check for double underscore pattern: locale_str[3] == '_'
        if locale_str[3] == '_':
            # Country is empty, variant starts at index 4
            if length < 5:
                # At least need language + "__" + variant (min 1 char) => length >= 4?
                # Actually, if length == 4, then language + "__" + one char variant, e.g., "fr__P"
                # That's valid. So we need to allow length >= 4.
                # But we already know length >= 4 because we checked length == 3 and length > 3.
                # So we can proceed.
                pass
            # variant is everything after the double underscore
            variant = locale_str[4:] if length > 4 else ""
            # variant could be empty? That would be language + "__" which is weird but maybe allowed?
            # In Java, "fr__" would produce language=fr, country='', variant=''.
            # We'll allow empty variant.
            return Locale(locale_str[0:2], "", variant)
        else:
            # Standard format: language_country or language_country_variant
            # Country is two uppercase letters at indices 3 and 4
            if length < 5:
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
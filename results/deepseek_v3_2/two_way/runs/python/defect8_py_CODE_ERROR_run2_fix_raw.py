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
        
        # Must have at least one underscore after language code
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # After language and underscore, we may have country, variant, or empty country.
        # We'll split by underscore and handle parts.
        parts = locale_str.split('_', 2)  # Split into max 3 parts: language, country, variant
        language = parts[0]
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            second = parts[1]
            if len(second) == 2 and second.isalpha() and second.isupper():
                # It's a country code
                country = second
                if len(parts) == 3:
                    variant = parts[2]
            else:
                # No country code, second part is variant (or empty if second is empty)
                if second == "":
                    # Handle double underscore: fr__POSIX -> language=fr, country="", variant="POSIX"
                    if len(parts) == 3:
                        variant = parts[2]
                else:
                    # Treat second as variant (e.g., fr_POSIX) though POSIX is usually after double underscore
                    variant = second
                    # If there is a third part, append with underscore? Actually split max 2, so third part is variant.
                    # But we already have variant from second, and third part would be extra.
                    # However, we split into max 3 parts, so third part is the rest after second underscore.
                    # In case of fr__POSIX, parts = ['fr', '', 'POSIX']
                    # In case of fr_POSIX, parts = ['fr', 'POSIX']
                    # In case of fr_FR_POSIX, parts = ['fr', 'FR', 'POSIX']
                    # So we need to handle when second is not a country code.
                    # If second is not empty and not a 2-char uppercase, treat as variant.
                    # And if there is a third part, it should be appended to variant? Actually variant is the third part.
                    # Wait: we split into max 3 parts, so if there are more underscores, they go into the third part.
                    # So variant can contain underscores.
                    # For fr_POSIX, parts[1] is 'POSIX', and there is no parts[2].
                    # For fr_FR_POSIX, parts[1] is 'FR', parts[2] is 'POSIX'.
                    # For fr__POSIX, parts[1] is '', parts[2] is 'POSIX'.
                    # So we already set variant appropriately.
                    pass
        
        return Locale(language, country, variant)
    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Validate language part (first two characters must be lowercase letters)
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # At least 3 characters, check for separator after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, that's just language + underscore (invalid)
        if length == 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have at least 4 characters: xx_?
        # Check if there is a country code (two uppercase letters) or another underscore (empty country)
        if length >= 5 and locale_str[3] != '_':
            # There is a country code at positions 3 and 4
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # Must have separator after country
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # Variant is everything after the second underscore
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
        else:
            # No country code (empty country) -> second underscore at position 3
            # So format is xx__variant
            if locale_str[3] != '_':
                # Actually, if length >=5 and we are here, we already know locale_str[3] != '_'? Wait.
                # Let's restructure: we are in the else branch meaning either length == 4 or locale_str[3] == '_'
                # But if length >=5 and locale_str[3] != '_', we would have entered the if branch.
                # So in this else branch, we have either:
                # - length == 4: xx_? (where ? is something, but we already know locale_str[2] == '_')
                #   If length == 4, then locale_str[3] is the only character after underscore.
                #   According to Java's Locale, after language there must be either country or variant.
                #   If there is only one character after underscore, it cannot be a country (needs two uppercase).
                #   So it must be a variant? But Java's Locale expects country then variant.
                #   Actually, Java's Locale constructor allows language, "", variant.
                #   The string representation is language + "_" + "_" + variant.
                #   So for length == 4, we have language + "_" + single character? That would be invalid.
                #   Because after first underscore, if there is no country, there must be another underscore.
                #   So we need to check for double underscore.
                # Let's simplify: after language and underscore, we look for either:
                #   - two uppercase letters (country) then optionally underscore and variant
                #   - another underscore (empty country) then variant
                # So we can check the character at index 3.
                pass
            # Actually, we need to handle the case where country is empty.
            # That means locale_str[3] == '_' (double underscore).
            # So we need to verify that.
            if length >= 4 and locale_str[3] == '_':
                # Empty country, variant starts at index 4
                if length == 4:
                    # Only double underscore, no variant -> invalid
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # Variant is everything after the second underscore
                return Locale(locale_str[0:2], "", locale_str[4:])
            else:
                # If length >=5 and locale_str[3] is not '_' and not uppercase letters, we already caught that.
                # For length == 4, if locale_str[3] is not '_', it's a single character after underscore.
                # That's invalid because country must be two uppercase letters or empty (double underscore).
                raise ValueError(f"Invalid locale format: {locale_str}")
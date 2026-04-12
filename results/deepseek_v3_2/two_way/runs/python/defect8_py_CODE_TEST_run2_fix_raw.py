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
        
        # Must have at least '_' after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, only language and underscore (e.g., "en_") -> treat as empty country and variant
        if length == 3:
            return Locale(locale_str[0:2], "")
        
        # Now we have at least 4 characters: language + '_' + something
        # Check if the next part is a country code (two uppercase letters) or another underscore (empty country)
        if length >= 5 and locale_str[3] != '_' and locale_str[4] != '_':
            # Possibly a country code: two uppercase letters
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z':
                # Valid country code
                if length == 5:
                    return Locale(locale_str[0:2], locale_str[3:5])
                # Check for variant separator
                if length >= 6 and locale_str[5] == '_':
                    variant = locale_str[6:] if length > 6 else ""
                    return Locale(locale_str[0:2], locale_str[3:5], variant)
                # If length >5 but no underscore at position 5, invalid
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If we reach here, either country is empty (next char is '_') or length is 4
        # Handle empty country with variant
        # locale_str format: ll_ _variant (two underscores) or ll_ (just underscore)
        # We already know position 2 is '_'
        if length == 4:
            # Only one character after first underscore, e.g., "en_X" -> invalid because country must be two letters or empty
            # But if that character is '_', then it's empty country and empty variant? Actually "en__" is language + empty country + empty variant.
            if locale_str[3] == '_':
                return Locale(locale_str[0:2], "", "")
            else:
                # Single character after underscore, not a valid country code (needs two uppercase) and not empty country.
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now length >= 5 and either country code not valid or we have empty country
        # Check if we have empty country (second underscore at position 3)
        if locale_str[3] == '_':
            # Empty country, variant starts after second underscore
            variant = locale_str[4:] if length > 4 else ""
            return Locale(locale_str[0:2], "", variant)
        
        # If we have a single character after first underscore and then underscore? e.g., "en_X_"
        # Actually we already handled length==4. For length>=5, if position 3 is not '_' and position 4 is '_', then we have a single-letter country? Not allowed.
        # So we need to check if position 4 is '_' and position 3 is a letter? That would be invalid because country must be two uppercase letters or empty.
        # Let's be strict: country must be exactly two uppercase letters or empty (represented by underscore).
        # So if we have something like "en_A_xxx", that's invalid because country is only one letter.
        # We already checked for two uppercase letters. If we didn't match that, and position 3 is not '_', then it's invalid.
        # But we also need to handle the case where country is missing and variant starts directly after first underscore? That would be "en_variant" which is not standard; we require two underscores for empty country.
        # According to Java Locale, the format is language_country_variant, where country and variant are optional. If country is missing, you still need two underscores? Actually Java's Locale.toString() returns "en__POSIX" for empty country and variant POSIX.
        # So we require that if country is empty, there must be two underscores.
        # Therefore, if length >=5 and position 3 is not '_' and we didn't get a valid two-letter country, it's invalid.
        raise ValueError(f"Invalid locale format: {locale_str}")
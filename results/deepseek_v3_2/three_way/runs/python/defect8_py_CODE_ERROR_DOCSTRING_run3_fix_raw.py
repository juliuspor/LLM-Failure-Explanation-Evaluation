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
        
        # Must have at least one underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # If length is 3, only language and underscore (invalid, but we handle gracefully?)
        if length == 3:
            # Only language and underscore, treat as language only? According to Java Locale, this is invalid.
            # But we can return language with empty country and variant.
            return Locale(locale_str[0:2], "")
        
        # Now we have at least 4 characters: language + '_' + something
        # Check if there is a country code (two uppercase letters) after the underscore
        if length >= 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z':
                # We have a valid country code
                country = locale_str[3:5]
                # Check for variant separator
                if length == 5:
                    return Locale(locale_str[0:2], country)
                else:
                    # There is more after country
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    variant = locale_str[6:] if length > 6 else ""
                    return Locale(locale_str[0:2], country, variant)
            else:
                # No country code, so the underscore after language is followed by variant
                # This handles the case like "fr__POSIX" where country is empty.
                # The variant starts after the first underscore (index 3 onwards)
                variant = locale_str[3:] if length > 3 else ""
                return Locale(locale_str[0:2], "", variant)
        else:
            # length is 4: language + '_' + one character (invalid country code)
            # Treat as language with empty country and variant starting after underscore
            variant = locale_str[3:]  # single character variant
            return Locale(locale_str[0:2], "", variant)
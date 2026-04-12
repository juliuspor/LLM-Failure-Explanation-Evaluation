    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Check first two characters are lowercase letters
        if length >= 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        
        # At least 3 characters, must have underscore at position 2
        if length >= 3 and locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Now we have language_...
        if length == 3:
            # Only language_ (trailing underscore) - treat as language only
            return Locale(locale_str[0:2], "")
        
        # length >= 4
        # Check if there is a country code (uppercase letters) after first underscore
        # Possibilities:
        # 1. language_XX (country code two uppercase letters)
        # 2. language_XX_... (country code then underscore and variant)
        # 3. language__... (empty country, variant after double underscore)
        
        # Look for second underscore to determine if country is present
        # We know locale_str[2] is '_'
        # Find next underscore starting from position 3
        second_underscore = locale_str.find('_', 3)
        
        if second_underscore == -1:
            # No second underscore, so the rest must be a 2-letter country code
            if length == 5:
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z':
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                # length != 5, invalid because country code must be exactly 2 letters
                raise ValueError(f"Invalid locale format: {locale_str}")
        else:
            # There is a second underscore
            # The part between first underscore (pos 2) and second underscore could be country code
            # If the part is empty (i.e., second_underscore == 3), then country is empty
            if second_underscore == 3:
                # Empty country, variant starts after second underscore
                variant = locale_str[second_underscore+1:]
                if len(variant) == 0:
                    # language__ (double underscore with no variant) - treat as language only
                    return Locale(locale_str[0:2], "")
                else:
                    return Locale(locale_str[0:2], "", variant)
            else:
                # There is something between underscores, must be 2-letter country code
                country_part = locale_str[3:second_underscore]
                if len(country_part) == 2:
                    ch3 = country_part[0]
                    ch4 = country_part[1]
                    if ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z':
                        variant = locale_str[second_underscore+1:]
                        return Locale(locale_str[0:2], country_part, variant)
                    else:
                        raise ValueError(f"Invalid locale format: {locale_str}")
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")

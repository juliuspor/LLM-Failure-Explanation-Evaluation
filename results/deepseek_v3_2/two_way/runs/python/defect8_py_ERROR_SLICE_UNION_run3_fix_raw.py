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
        
        # At least 3 characters, check for separator
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 3:
            # Only language and underscore (e.g., "fr_")
            return Locale(locale_str[0:2], "")
        
        # Now we have at least 4 characters: language + "_" + something
        # The part after the first underscore could be country, variant, or empty country then variant.
        # We need to parse according to the pattern: language + "_" + country? + "_"? + variant?
        # where country is exactly two uppercase letters (optional) and variant is everything after second underscore.
        
        # Find the second underscore if any
        second_underscore = locale_str.find('_', 3)
        
        if second_underscore == -1:
            # No second underscore: format is language_country where country length must be 2
            if length == 5:
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if 'A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z':
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                # length != 5: could be language + "_" + something not 2 chars
                # According to Java Locale, country must be exactly 2 uppercase letters.
                # But we also need to support cases like "fr__POSIX" where country is empty.
                # Actually, if there's no second underscore, the entire part after first underscore
                # must be exactly 2 uppercase letters. Otherwise it's invalid.
                # However, the bug is about "fr__POSIX" which has two underscores.
                # So we can fall through to the else case with second_underscore != -1.
                # But if length !=5 and no second underscore, it's invalid.
                raise ValueError(f"Invalid locale format: {locale_str}")
        else:
            # There is a second underscore.
            # The part between first and second underscore could be country (2 uppercase) or empty.
            country_part = locale_str[3:second_underscore]
            variant_part = locale_str[second_underscore+1:]
            
            # Validate country part if present
            if country_part:
                if len(country_part) == 2:
                    ch3 = country_part[0]
                    ch4 = country_part[1]
                    if 'A' <= ch3 <= 'Z' and 'A' <= ch4 <= 'Z':
                        return Locale(locale_str[0:2], country_part, variant_part)
                    else:
                        raise ValueError(f"Invalid locale format: {locale_str}")
                else:
                    # country part length not 2
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                # Empty country part (like "fr__POSIX")
                return Locale(locale_str[0:2], "", variant_part)
    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if length == 2:
            return Locale(locale_str, "")
        else:
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            
            if length == 3:
                # Only language and underscore (e.g., "en_")? Treat as language only.
                return Locale(locale_str[0:2], "")
            
            # Check if there is a country code (two uppercase letters) after the first underscore
            if length >= 5 and locale_str[3] != '_' and locale_str[4] != '_':
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                
                if length == 5:
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
            else:
                # No country code (double underscore) or country code missing.
                # The next character after the first underscore is either another underscore or there is no country.
                # So country is empty, and the rest is variant.
                # The variant starts after the second underscore (if present) or after the first underscore if length is 4? Actually, we need to handle cases like "fr__POSIX" (length 9) where positions: 0=f,1=r,2=_,3=_,4=P,5=O,6=S,7=I,8=X.
                # So country is empty, variant starts at index 4? Wait, after the double underscore, the variant is from index 4 onward.
                # But we also have to consider the case where there is only one underscore and then variant? That would be like "fr_POSIX" (length 8) which should be language "fr", country "POSIX"? Actually, country must be two uppercase letters, so "POSIX" is not a valid country. So that should be invalid. However, the original Java Locale allows a variant after a single underscore? In Java, the format is language_country_variant, where country is optional but if variant is present and country is missing, you need two underscores? Actually, Java's Locale constructor expects language, country, variant. The string representation is language + (country.isEmpty() ? "" : "_" + country) + (variant.isEmpty() ? "" : "_" + variant). So if country is empty and variant is not, you get two underscores. So we should enforce that.
                # So if after the first underscore we don't have two uppercase letters, then we assume country is empty and the next character must be '_' (second underscore) and then variant.
                # Let's check: if length >= 4 and locale_str[3] == '_':
                # Then country = "", variant starts at index 4.
                # If length >= 4 and locale_str[3] != '_', then we need to check if it's a valid country code (two uppercase letters). Already handled above.
                # So for double underscore, we have locale_str[3] == '_'.
                if length >= 4 and locale_str[3] == '_':
                    # Double underscore: country empty, variant starts at index 4.
                    return Locale(locale_str[0:2], "", locale_str[4:])
                else:
                    # The string has at least 4 characters, but the character at index 3 is not an underscore and not a valid uppercase letter (or we wouldn't be here).
                    # This could be a malformed locale like "fr_POSIX" where POSIX is not two letters. We should reject.
                    raise ValueError(f"Invalid locale format: {locale_str}")
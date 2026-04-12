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
            
            # Check if there is a country code (uppercase letters) after the first underscore
            if length >= 5 and locale_str[3] != '_':
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = locale_str[3:5]
                # Now check for variant after second underscore
                if length == 5:
                    return Locale(locale_str[0:2], country)
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    variant = locale_str[6:]
                    return Locale(locale_str[0:2], country, variant)
            else:
                # No country code (double underscore) or length < 5
                # The next character after first underscore is either '_' or end of string
                if length == 3:
                    # Only language and underscore (e.g., "fr_") - treat as no country, no variant
                    return Locale(locale_str[0:2], "")
                else:
                    # There is at least a second underscore
                    if locale_str[3] != '_':
                        # Actually, if length >=4 and locale_str[3] is not '_', it should be country code
                        # But we already handled that above. So this case is when locale_str[3] == '_'
                        pass
                    # Now we have double underscore, variant starts after second underscore
                    if length == 4:
                        # Only language and double underscore, no variant (e.g., "fr__")
                        return Locale(locale_str[0:2], "", "")
                    else:
                        # variant starts at index 4? Wait: indices: 0=f,1=r,2=_,3=_,4=P (for "fr__POSIX")
                        # Actually, after double underscore, variant starts at index 4.
                        # But we already know locale_str[3] is '_', so variant is from index 4 onward.
                        variant = locale_str[4:]
                        return Locale(locale_str[0:2], "", variant)
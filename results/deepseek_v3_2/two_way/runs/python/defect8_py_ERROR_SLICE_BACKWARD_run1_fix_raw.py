    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Handle special case for POSIX locale
        if locale_str == "POSIX" or locale_str == "C":
            return Locale("", "", "POSIX")
        
        # Check for double underscore separating language and variant (e.g., "fr__POSIX")
        parts = locale_str.split('_')
        if len(parts) == 3 and parts[1] == "":
            # Format: language + "_" + "_" + variant (e.g., "fr__POSIX")
            language = parts[0]
            variant = parts[2]
            if len(language) == 2 and language.isalpha() and language.islower():
                return Locale(language, "", variant)
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Original logic for standard formats
        length = len(locale_str)
        if length != 2 and length != 5 and length < 7:
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
    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length == 2:
            # Validate two lowercase letters
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        elif length >= 5:
            # Validate first two characters are lowercase letters
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Check for underscore at position 2
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Validate next two characters are uppercase letters
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # Length > 5, must have underscore at position 5
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
        else:
            # Length is 0, 1, 3, or 4 (or negative, but len won't return negative)
            raise ValueError(f"Invalid locale format: {locale_str}")
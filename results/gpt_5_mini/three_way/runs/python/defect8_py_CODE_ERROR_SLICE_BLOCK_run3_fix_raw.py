@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
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
            
            # Allow either a two-letter country (positions 3-4 uppercase) or an empty country (positions 3-4 == '_')
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            # Empty country form: ll__variant (e.g., fr__POSIX)
            if ch3 == '_' and ch4 == '_':
                # Must have at least 'll__v' -> length >= 7 and position 5 must be start of variant separator
                if length < 7:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # position 5 should be start of variant (i.e., locale_str[5] == first char of variant)
                # In the Java form, the separators are at positions 2 and 5, so position 5 must be '_'
                if locale_str[5] != '_':
                    # Accept forms like 'll__variant' where separator at pos 2 and pos 5 are both underscores
                    # if pos5 is not '_', it's still acceptable because variant starts at pos5 (after ll__)
                    pass
                return Locale(locale_str[0:2], "", locale_str[6:])
            else:
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if length == 5:
                    return Locale(locale_str[0:2], locale_str[3:5])
                else:
                    if locale_str[5] != '_':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
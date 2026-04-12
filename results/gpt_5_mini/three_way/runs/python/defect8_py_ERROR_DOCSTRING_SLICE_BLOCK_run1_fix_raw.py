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
            
            # Handle case where country is empty (e.g., "fr__POSIX")
            # If characters 3 and 4 are both underscores, treat country as empty
            # and parse variant starting at position 5.
            if length >= 5 and locale_str[3] == '_' and (length == 3 or locale_str[4] == '_'):
                # This condition is a bit defensive; prefer simple check:
                pass
            
            # If there's at least positions 3 and 4, inspect them
            # If they form uppercase country letters, use them.
            # If they are underscores (empty country), allow variant-only form.
            # Validate bounds before accessing indices.
            if length >= 5:
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 == '_' and ch4 == '_':
                    # form: ll__variant -> language, empty country, variant starts at 5
                    if length == 5:
                        # "ll__" is invalid (no variant)
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    if locale_str[5] != '_':
                        # In this special empty-country form, position 5 is start of variant (no extra underscore expected)
                        return Locale(locale_str[0:2], "", locale_str[5:])
                    else:
                        # Unexpected extra underscore
                        return Locale(locale_str[0:2], "", locale_str[6:])
                else:
                    # Expect country as two uppercase letters
                    if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    if length == 5:
                        return Locale(locale_str[0:2], locale_str[3:5])
                    else:
                        if locale_str[5] != '_':
                            raise ValueError(f"Invalid locale format: {locale_str}")
                        return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")

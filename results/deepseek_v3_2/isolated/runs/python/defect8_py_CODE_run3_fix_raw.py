    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        length = len(locale_str)
        if length == 2:
            # Language only
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        elif length >= 5:
            # At least language_country, possibly with variant
            # Check language part
            if locale_str[0] < 'a' or locale_str[0] > 'z' or locale_str[1] < 'a' or locale_str[1] > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Check country part
            if locale_str[3] < 'A' or locale_str[3] > 'Z' or locale_str[4] < 'A' or locale_str[4] > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 5:
                return Locale(locale_str[0:2], locale_str[3:5])
            else:
                # length >= 6
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # variant is everything after the second underscore
                variant = locale_str[6:] if length > 6 else ""
                return Locale(locale_str[0:2], locale_str[3:5], variant)
        else:
            # length 0, 1, 3, 4 (or negative) are invalid
            raise ValueError(f"Invalid locale format: {locale_str}")
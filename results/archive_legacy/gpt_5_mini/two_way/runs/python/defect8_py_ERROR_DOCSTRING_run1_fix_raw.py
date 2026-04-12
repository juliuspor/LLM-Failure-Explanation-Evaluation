@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        if length >= 3:
            ch0 = locale_str[0]
            ch1 = locale_str[1]
            if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if length == 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            # find next underscore if any
            if '_' not in locale_str[3:]:
                country = locale_str[3:]
                if country == "":
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if len(country) != 2:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if country[0] < 'A' or country[0] > 'Z' or country[1] < 'A' or country[1] > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], country)
            else:
                idx = locale_str.find('_', 3)
                country = locale_str[3:idx]
                variant = locale_str[idx+1:]
                if country != "":
                    if len(country) != 2:
                        raise ValueError(f"Invalid locale format: {locale_str}")
                    if country[0] < 'A' or country[0] > 'Z' or country[1] < 'A' or country[1] > 'Z':
                        raise ValueError(f"Invalid locale format: {locale_str}")
                if variant == "":
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], country, variant)
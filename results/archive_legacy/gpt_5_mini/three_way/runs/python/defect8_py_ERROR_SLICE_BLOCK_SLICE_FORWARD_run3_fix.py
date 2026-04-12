@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        if length != 2 and length != 5 and length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")
        parts = locale_str.split('_', 2)
        if len(parts[0]) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        lang0 = parts[0]
        if not ('a' <= lang0[0] <= 'z' and 'a' <= lang0[1] <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 1:
            return Locale(lang0, "")
        if len(parts) == 2:
            country = parts[1]
            if country == "":
                return Locale(lang0, "")
            if len(country) != 2 or not ('A' <= country[0] <= 'Z' and 'A' <= country[1] <= 'Z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang0, country)
        country = parts[1]
        variant = parts[2]
        if country != "":
            if len(country) != 2 or not ('A' <= country[0] <= 'Z' and 'A' <= country[1] <= 'Z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang0, country, variant)
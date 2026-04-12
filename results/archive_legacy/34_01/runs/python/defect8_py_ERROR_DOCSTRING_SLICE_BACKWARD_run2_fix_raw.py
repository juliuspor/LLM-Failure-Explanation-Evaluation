@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        if len(parts) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if len(language) != 2 or not ('a' <= language[0] <= 'z') or not ('a' <= language[1] <= 'z'):
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = ""
        variant = ""
        if len(parts) == 1:
            return Locale(language, country, variant)
        if len(parts) == 2:
            country = parts[1]
            if country == "":
                return Locale(language, "", "")
            if len(country) != 2 or not ('A' <= country[0] <= 'Z') or not ('A' <= country[1] <= 'Z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, "")
        country = parts[1]
        variant = parts[2]
        if country != "":
            if len(country) != 2 or not ('A' <= country[0] <= 'Z') or not ('A' <= country[1] <= 'Z'):
                raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)
@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_', 2)
        # parts can be ['ll'], ['ll','CC'], ['ll','','VAR'], ['ll','CC','VAR']
        if len(parts[0]) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        lang = parts[0]
        if not (lang[0].islower() and lang[1].islower() and lang.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(parts) == 1:
            return Locale(lang, "")
        country = parts[1]
        if country:
            if len(country) != 2 or not (country[0].isupper() and country[1].isupper() and country.isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
        # if there's a variant part
        if len(parts) == 3:
            variant = parts[2]
            if variant == "":
                # empty variant is allowed? treat as invalid
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country, variant)
        # only language and country
        return Locale(lang, country)
    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if len(parts) == 1:
            # Single part: language only
            if len(parts[0]) == 2 and parts[0].isalpha() and parts[0].islower():
                return Locale(parts[0], "")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        elif len(parts) == 2:
            # Two parts: language and country, or language and variant (if country empty)
            lang, second = parts
            if len(lang) == 2 and lang.isalpha() and lang.islower():
                if len(second) == 2 and second.isalpha() and second.isupper():
                    # language and country
                    return Locale(lang, second)
                elif len(second) > 0:
                    # language and variant (empty country)
                    return Locale(lang, "", second)
                else:
                    # second part empty (e.g., "fr_") - invalid
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        elif len(parts) == 3:
            # Three parts: language, country, variant
            lang, country, variant = parts
            if len(lang) == 2 and lang.isalpha() and lang.islower():
                if len(country) == 2 and country.isalpha() and country.isupper():
                    return Locale(lang, country, variant)
                elif len(country) == 0:
                    # empty country (e.g., "fr__POSIX")
                    return Locale(lang, "", variant)
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")
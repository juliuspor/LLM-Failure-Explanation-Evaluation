    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_')
        if len(parts) == 1:
            # Only language
            if len(parts[0]) == 2 and parts[0].isalpha() and parts[0].islower():
                return Locale(parts[0], "")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        elif len(parts) == 2:
            # language and country, or language and variant (if country empty)
            lang, second = parts
            if len(lang) == 2 and lang.isalpha() and lang.islower():
                if len(second) == 2 and second.isalpha() and second.isupper():
                    # language + country
                    return Locale(lang, second)
                else:
                    # language + variant (country empty)
                    return Locale(lang, "", second)
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        elif len(parts) == 3:
            # language, country, variant
            lang, country, variant = parts
            if len(lang) == 2 and lang.isalpha() and lang.islower():
                if len(country) == 2 and country.isalpha() and country.isupper():
                    return Locale(lang, country, variant)
                elif country == "":
                    # double underscore case: fr__POSIX
                    return Locale(lang, "", variant)
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        else:
            # More than three parts? treat extra parts as part of variant
            lang = parts[0]
            if len(lang) == 2 and lang.isalpha() and lang.islower():
                if len(parts[1]) == 2 and parts[1].isalpha() and parts[1].isupper():
                    country = parts[1]
                    variant = '_'.join(parts[2:])
                    return Locale(lang, country, variant)
                elif parts[1] == "":
                    # double underscore with multi-part variant
                    country = ""
                    variant = '_'.join(parts[2:])
                    return Locale(lang, country, variant)
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
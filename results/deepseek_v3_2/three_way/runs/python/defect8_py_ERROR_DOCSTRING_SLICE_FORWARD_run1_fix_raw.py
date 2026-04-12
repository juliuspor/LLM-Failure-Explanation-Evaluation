    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        parts = locale_str.split('_')
        if len(parts) == 1:
            # Only language
            lang = parts[0]
            if len(lang) != 2 or not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, "")
        elif len(parts) == 2:
            # language and country, or language and variant (if country missing)
            lang, second = parts
            if len(lang) != 2 or not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(second) == 2 and second.isalpha() and second.isupper():
                # language_country
                return Locale(lang, second)
            else:
                # language__variant (country missing)
                return Locale(lang, "", second)
        elif len(parts) == 3:
            # language_country_variant
            lang, country, variant = parts
            if len(lang) != 2 or not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if country:
                if len(country) != 2 or not country.isalpha() or not country.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(lang, country, variant)
        else:
            # More than three parts (e.g., language_country_variant_extra)
            lang = parts[0]
            if len(lang) != 2 or not lang.isalpha() or not lang.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            country = parts[1] if len(parts) > 1 and len(parts[1]) == 2 and parts[1].isalpha() and parts[1].isupper() else ""
            variant = '_'.join(parts[2:]) if len(parts) > 2 else ""
            return Locale(lang, country, variant)
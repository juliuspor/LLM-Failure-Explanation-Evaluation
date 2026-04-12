    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if len(parts) == 1:
            # Only language part
            language = parts[0]
            if len(language) != 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "")
        elif len(parts) == 2:
            # Language and country, or language and variant (if country is empty)
            language, second = parts
            if len(language) != 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(second) == 2 and second.isalpha() and second.isupper():
                # Second part is a country code
                return Locale(language, second)
            else:
                # Second part is a variant (country is empty)
                return Locale(language, "", second)
        elif len(parts) == 3:
            # Language, country, variant (country may be empty)
            language, country, variant = parts
            if len(language) != 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if country:
                if len(country) != 2 or not country.isalpha() or not country.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
            # Variant can be any non‑empty string
            if not variant:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")
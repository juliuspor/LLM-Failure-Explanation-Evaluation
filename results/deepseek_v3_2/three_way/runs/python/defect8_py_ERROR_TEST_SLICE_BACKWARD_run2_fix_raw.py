    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if len(parts) == 1:
            # language only
            language = parts[0]
            if len(language) != 2 and len(language) != 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "")
        elif len(parts) == 2:
            # language and country, or language and variant (if country empty)
            language = parts[0]
            second = parts[1]
            if len(language) != 2 and len(language) != 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Check if second part is a country code (2 letters uppercase) or a variant
            if len(second) == 2 and second.isalpha() and second.isupper():
                # language_country
                return Locale(language, second)
            else:
                # language__variant (empty country)
                # second is the variant, country is empty
                return Locale(language, "", second)
        elif len(parts) == 3:
            # language_country_variant
            language, country, variant = parts
            if len(language) != 2 and len(language) != 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 and len(country) != 3:
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
        else:
            # More than 3 parts? Not supported.
            raise ValueError(f"Invalid locale format: {locale_str}")
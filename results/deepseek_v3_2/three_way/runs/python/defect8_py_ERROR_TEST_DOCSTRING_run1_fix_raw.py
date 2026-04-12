    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Split by underscore, but keep empty parts to handle double underscores
        parts = locale_str.split('_')
        
        # Validate the number of parts: 1 (language), 2 (language and country), or 3 (language, country, variant)
        # But also allow 3 parts with empty country (double underscore)
        if len(parts) == 1:
            # Just language
            language = parts[0]
            if len(language) != 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, "")
        elif len(parts) == 2:
            # language and country (or language and variant if country empty? Not allowed by standard)
            language, country = parts
            if len(language) != 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country)
        elif len(parts) == 3:
            language, country, variant = parts
            if len(language) != 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            # Country can be empty (double underscore) or exactly 2 uppercase letters
            if country == "":
                # Empty country, variant present
                pass
            elif len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")
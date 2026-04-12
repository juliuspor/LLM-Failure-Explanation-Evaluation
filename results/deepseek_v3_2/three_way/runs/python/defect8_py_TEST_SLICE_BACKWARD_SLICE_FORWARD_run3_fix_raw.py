    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts or not parts[0]:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0].lower()
        if len(language) != 2 and len(language) != 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            # Second part could be country or variant if empty country
            if parts[1] == "":
                # Double underscore case: country is empty, variant starts at parts[2]
                if len(parts) >= 3:
                    variant = '_'.join(parts[2:])
                else:
                    # Just double underscore with no variant? treat as empty variant
                    pass
            else:
                country = parts[1].upper()
                if len(country) != 2 and len(country) != 3:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if not country.isalpha() and not country.isdigit():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if len(parts) >= 3:
                    variant = '_'.join(parts[2:])
        
        return Locale(language, country, variant)
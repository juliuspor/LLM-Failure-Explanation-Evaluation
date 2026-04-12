    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if len(parts) == 0 or len(parts[0]) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0].lower()
        if not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            if len(parts[1]) == 2:
                country = parts[1].upper()
                if not country.isalpha() or not country.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if len(parts) >= 3:
                    variant = '_'.join(parts[2:])
            else:
                # Country is empty, second part is actually the variant
                variant = '_'.join(parts[1:])
        
        return Locale(language, country, variant)
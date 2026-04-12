    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts or not parts[0] or len(parts[0]) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        if len(parts) > 1:
            if parts[1]:
                if len(parts[1]) == 2 and parts[1].isalpha() and parts[1].isupper():
                    country = parts[1]
                else:
                    variant = parts[1]
            if len(parts) > 2:
                variant = '_'.join(parts[2:])
        
        return Locale(language, country, variant)
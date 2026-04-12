    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_', 2)  # Split into max 3 parts
        language = parts[0]
        country = ''
        variant = ''
        
        if len(language) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if len(parts) > 1:
            second = parts[1]
            if second == '':
                # Empty country part (double underscore) is allowed
                country = ''
            else:
                if len(second) != 2:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if not second.isalpha() or not second.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = second
        
        if len(parts) > 2:
            variant = parts[2]
        
        return Locale(language, country, variant)
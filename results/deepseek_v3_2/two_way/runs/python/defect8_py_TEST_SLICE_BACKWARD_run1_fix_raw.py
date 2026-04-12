    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not (1 <= len(parts) <= 3):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            second = parts[1]
            if second == "":  # Empty country (language__variant)
                if len(parts) == 3:
                    variant = parts[2]
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
            elif len(second) == 2 and second.isalpha() and second.isupper():
                country = second
                if len(parts) == 3:
                    variant = parts[2]
            else:
                # Second part is not a valid country code, treat as variant
                variant = second
                if len(parts) == 3:
                    raise ValueError(f"Invalid locale format: {locale_str}")
        
        return Locale(language, country, variant)
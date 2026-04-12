    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts or len(parts[0]) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0].lower()
        if len(language) != 2 or not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        if len(parts) > 1:
            # Second part could be country or variant if country is missing
            if len(parts[1]) == 2 and parts[1].isalpha():
                country = parts[1].upper()
                if len(parts) > 2:
                    variant = '_'.join(parts[2:])
            else:
                # No country, second part is variant
                variant = '_'.join(parts[1:])
        
        return Locale(language, country, variant)
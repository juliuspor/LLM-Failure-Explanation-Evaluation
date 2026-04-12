    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if not language or len(language) < 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) > 1:
            # second part could be country or variant if empty country
            second = parts[1]
            if second == "":
                # double underscore, country is empty, variant is parts[2] if exists
                if len(parts) > 2:
                    variant = '_'.join(parts[2:])
                else:
                    # only language and empty country, no variant
                    pass
            else:
                # second part is non-empty
                if len(second) == 2 and second.isalpha() and second.isupper():
                    country = second
                    if len(parts) > 2:
                        variant = '_'.join(parts[2:])
                else:
                    # second part is not a valid country code, treat as variant
                    country = ""
                    variant = '_'.join(parts[1:])
        
        return Locale(language, country, variant)
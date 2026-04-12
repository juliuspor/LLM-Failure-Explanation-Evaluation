    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Handle empty string
        if not locale_str:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Split by underscore, preserving empty segments for double underscores
        parts = locale_str.split('_')
        
        # Validate language part (first part)
        if len(parts) == 0 or not parts[0]:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if len(language) < 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Initialize country and variant
        country = ""
        variant = ""
        
        if len(parts) == 1:
            # Only language
            return Locale(language, "", "")
        elif len(parts) == 2:
            # language + country OR language + variant (if country empty)
            second = parts[1]
            if second == "":
                # This would be a trailing underscore, which is invalid
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(second) == 2 and second.isalpha() and second.isupper():
                # Two-letter uppercase -> country
                country = second
            else:
                # Treat as variant (country empty)
                variant = second
        elif len(parts) == 3:
            # language + country + variant OR language + empty country + variant
            second = parts[1]
            third = parts[2]
            if second == "":
                # Double underscore: language + empty country + variant
                country = ""
                variant = third
            else:
                # Normal case: language + country + variant
                if len(second) != 2 or not second.isalpha() or not second.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                country = second
                variant = third
        else:
            # More than three parts (e.g., language__variant_extra) not supported
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        return Locale(language, country, variant)
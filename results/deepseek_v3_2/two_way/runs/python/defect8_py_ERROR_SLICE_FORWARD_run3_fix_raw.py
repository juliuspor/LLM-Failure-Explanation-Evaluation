    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_', 2)  # Split into at most 3 parts
        
        # Validate language part (first part)
        if len(parts) == 0 or len(parts[0]) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if len(language) < 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            # Second part could be country or variant if empty country
            second = parts[1]
            if len(second) == 0:
                # Empty country, treat as variant in third part if exists
                if len(parts) >= 3:
                    variant = parts[2]
                else:
                    # Only language and empty country? Not valid.
                    raise ValueError(f"Invalid locale format: {locale_str}")
            elif len(second) == 2 and second.isalpha() and second.isupper():
                country = second
                if len(parts) == 3:
                    variant = parts[2]
            else:
                # Second part is not a valid country code, treat as variant
                variant = second
                if len(parts) == 3:
                    # If there's a third part, append to variant with underscore?
                    # According to Java Locale, variant can contain multiple segments separated by underscore.
                    # But we split into max 3 parts, so third part is part of variant.
                    variant = second + '_' + parts[2]
        
        return Locale(language, country, variant)
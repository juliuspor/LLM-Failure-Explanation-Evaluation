    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Handle empty string
        if not locale_str:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Split by underscore
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
        
        # Process remaining parts
        if len(parts) > 1:
            # Second part could be country or variant if empty country
            second = parts[1]
            if second == "":
                # Empty country, meaning double underscore, so second part is actually variant
                # Example: "fr__POSIX" -> parts = ['fr', '', 'POSIX']
                # Country remains empty, variant is the third part if exists
                if len(parts) > 2:
                    variant = parts[2]
                else:
                    # Only double underscore with no variant? e.g., "fr__"
                    # This is invalid because variant is empty? But we can treat as no variant.
                    pass
            else:
                # Second part is non-empty
                if len(second) == 2 and second.isalpha() and second.isupper():
                    country = second
                    # Check for variant in third part
                    if len(parts) > 2:
                        variant = parts[2]
                else:
                    # Second part is not a valid country code, treat as variant
                    # This handles cases like "fr_POSIX" where POSIX is variant (country empty)
                    country = ""
                    variant = second
                    # If there are more parts, append them with underscore? Usually variant can contain underscores.
                    # According to Java Locale, variant can be any string, may contain multiple underscores.
                    # So we should join remaining parts with underscore.
                    if len(parts) > 2:
                        variant = '_'.join(parts[1:])
        
        # Additional validation: if country is provided, must be 2 letters uppercase
        if country and (len(country) != 2 or not country.isalpha() or not country.isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        return Locale(language, country, variant)
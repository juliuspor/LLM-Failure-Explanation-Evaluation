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
            # Second part could be country or variant if country is missing
            second = parts[1]
            if second == "":
                # Handle double underscore (empty country) like "fr__POSIX"
                # The empty string indicates no country, so second part is actually variant if present
                if len(parts) > 2:
                    variant = parts[2]
                else:
                    # Only language and empty country, no variant
                    pass
            else:
                # Check if second part looks like a country code (2 letters uppercase or 3 digits)
                if len(second) == 2 and second.isalpha() and second.isupper():
                    country = second
                    if len(parts) > 2:
                        variant = parts[2]
                elif len(second) == 3 and second.isdigit():
                    # UN M.49 numeric-3 area code
                    country = second
                    if len(parts) > 2:
                        variant = parts[2]
                else:
                    # Second part is not a country code, treat as variant
                    country = ""
                    variant = second
                    # If there are more parts, join them as variant? Usually variant is a single part.
                    # But spec says variant is any arbitrary value. We'll join remaining parts with '_'
                    if len(parts) > 2:
                        variant = '_'.join(parts[1:])
        
        # Validate country if present
        if country:
            if not (len(country) == 2 and country.isalpha() and country.isupper()) and not (len(country) == 3 and country.isdigit()):
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        return Locale(language, country, variant)
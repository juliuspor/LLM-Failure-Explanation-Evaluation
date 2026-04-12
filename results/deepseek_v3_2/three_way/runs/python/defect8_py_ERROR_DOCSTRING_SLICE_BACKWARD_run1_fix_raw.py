    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Handle special case for POSIX locale
        if locale_str == "POSIX" or locale_str == "C":
            return Locale("", "", "POSIX")
        
        parts = locale_str.split('_')
        if len(parts) == 0 or len(parts) > 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        country = ""
        variant = ""
        
        if len(language) != 2 and len(language) != 3:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if len(parts) >= 2:
            country = parts[1]
            if len(country) == 0:
                # Handle double underscore (e.g., "fr__POSIX")
                if len(parts) >= 3:
                    variant = parts[2]
                else:
                    variant = ""
                country = ""
            elif len(country) == 2:
                if not country.isalpha() or not country.isupper():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if len(parts) == 3:
                    variant = parts[2]
            else:
                # Country code can be 3 digits (UN M.49) or special like "POSIX"
                if country.isdigit() and len(country) == 3:
                    # numeric country code
                    pass
                else:
                    # treat as variant if country is not 2 letters
                    variant = country
                    country = ""
                if len(parts) == 3:
                    # If we already used country as variant, the third part is extra variant
                    variant = variant + "_" + parts[2] if variant else parts[2]
        
        # Additional validation for variant (if any)
        if variant:
            # Variant can be any string, but we should ensure no extra underscores?
            # Already handled by split.
            pass
        
        return Locale(language, country, variant)
    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        # Handle empty string
        if not locale_str:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Split by underscore
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0].lower()
        if len(language) != 2 or not language.isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            # Second part could be country or variant if empty country
            second = parts[1]
            if second == "":
                # Empty country, so second part is actually variant if exists
                # This handles double underscore case
                if len(parts) >= 3:
                    variant = parts[2]
                else:
                    # Only language and empty country, no variant
                    pass
            else:
                # Check if second part looks like a country code (2 letters or 3 digits)
                if len(second) == 2 and second.isalpha():
                    country = second.upper()
                elif len(second) == 3 and second.isdigit():
                    country = second  # UN M.49 numeric code
                else:
                    # Not a country code, treat as variant
                    variant = second
                    # If there are more parts, join them as variant?
                    # According to Java Locale, variant can have underscores.
                    # But the original method only expected three parts total.
                    # We'll follow the original pattern: variant is everything after country.
                    # Since we treat second as variant, we need to join remaining parts.
                    if len(parts) > 2:
                        variant = '_'.join(parts[1:])
                    else:
                        variant = second
                    country = ""
        
        # If we haven't set variant yet, check remaining parts
        if not variant and len(parts) >= 3:
            # Country was set, so parts[2] is variant
            variant = parts[2]
            # If there are more parts, join them as variant (since variant can contain underscores)
            if len(parts) > 3:
                variant = '_'.join(parts[2:])
        
        # Validate country if present
        if country:
            if len(country) == 2:
                if not country.isalpha():
                    raise ValueError(f"Invalid locale format: {locale_str}")
            elif len(country) == 3:
                if not country.isdigit():
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        return Locale(language, country, variant)
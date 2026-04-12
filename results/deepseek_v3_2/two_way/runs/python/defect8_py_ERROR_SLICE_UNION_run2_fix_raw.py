    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if len(language) != 2 or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            country_part = parts[1]
            if country_part:
                if len(country_part) == 2 and country_part.isalpha() and country_part.isupper():
                    country = country_part
                else:
                    # Could be a variant if country is empty (like POSIX)
                    # In Java's Locale, POSIX is a variant, not a country.
                    # So we treat this as variant if country is empty.
                    # But we need to handle cases like "fr__POSIX" where country is empty.
                    # Actually, if parts[1] is empty, then we have double underscore.
                    # We'll skip empty parts.
                    pass
        
        # Reconstruct variant from remaining parts
        # Skip empty parts (from double underscores)
        non_empty_parts = [p for p in parts if p]
        if len(non_empty_parts) >= 2:
            # The second non-empty part could be country or variant
            second = non_empty_parts[1]
            if second.isupper() and len(second) == 2:
                country = second
                if len(non_empty_parts) >= 3:
                    variant = '_'.join(non_empty_parts[2:])
            else:
                # If not a two-letter uppercase, treat as variant
                variant = '_'.join(non_empty_parts[1:])
        
        return Locale(language, country, variant)
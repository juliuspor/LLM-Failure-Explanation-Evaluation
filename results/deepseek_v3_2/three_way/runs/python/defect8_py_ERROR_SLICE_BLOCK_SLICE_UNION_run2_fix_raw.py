    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if not parts:
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        language = parts[0]
        if not language:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if len(language) != 2 or not language.isalpha() or not language.islower():
            # Language must be 2 letters, lowercase (ISO 639 alpha-2).
            # We could also allow 3 letters (alpha-3), but the original code only allowed 2.
            # However, to be more flexible, we allow 2 or 3 letters.
            if len(language) != 3 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
        
        country = ""
        variant = ""
        
        if len(parts) >= 2:
            second = parts[1]
            if second:
                # Second part could be country or variant (if country is empty).
                # According to POSIX, a locale like "fr__POSIX" has empty country.
                # So if second part is all uppercase and length 2, treat as country.
                # Otherwise, treat as variant.
                if len(second) == 2 and second.isalpha() and second.isupper():
                    country = second
                    if len(parts) >= 3:
                        variant = '_'.join(parts[2:])
                else:
                    # No country, second part is variant
                    variant = '_'.join(parts[1:])
            else:
                # Second part is empty (double underscore), so country is empty.
                if len(parts) >= 3:
                    variant = '_'.join(parts[2:])
                else:
                    # Only language and empty part? That's invalid.
                    raise ValueError(f"Invalid locale format: {locale_str}")
        
        return Locale(language, country, variant)
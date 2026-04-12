    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_', 2)  # Split into at most 3 parts
        language = parts[0]
        country = ""
        variant = ""
        
        if len(language) != 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        if len(parts) >= 2:
            # Second part could be country or variant if empty country
            second = parts[1]
            if len(second) == 2 and second.isalpha() and second.isupper():
                country = second
                if len(parts) == 3:
                    variant = parts[2]
            else:
                # No country, second part is variant
                variant = second
                # If there is a third part, it's part of variant (should not happen due to split limit)
                # but we already split into max 3 parts, so parts[2] would be empty if there were more underscores?
                # Actually, split('_', 2) ensures at most 3 parts; if there are more underscores, they go into parts[2]
                # So variant already includes everything after the second underscore.
                # However, we need to handle the case where second part is empty (double underscore).
                # In that case, second == '' and we should treat it as empty country, and variant is parts[2] if exists.
                if second == '':
                    # This is the case of double underscore: language__variant
                    if len(parts) == 3:
                        variant = parts[2]
                    else:
                        # Actually, if second is empty and there is no third part, that's just language_
                        # But that's invalid because trailing underscore? We'll treat as language only.
                        # However, the original code would have raised ValueError. We'll mimic that.
                        # But the bug report is about fr__POSIX, which has variant.
                        # So we need to allow empty country and variant.
                        pass
        
        # Validate country if present
        if country and (len(country) != 2 or not country.isalpha() or not country.isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        
        # Variant can be anything, no validation needed.
        
        return Locale(language, country, variant)
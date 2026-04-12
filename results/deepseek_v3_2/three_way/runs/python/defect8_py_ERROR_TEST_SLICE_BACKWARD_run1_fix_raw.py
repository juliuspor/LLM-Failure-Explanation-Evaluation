    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if len(parts) == 1:
            # language only
            language = parts[0]
            if len(language) == 2 and language.isalpha() and language.islower():
                return Locale(language, "")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        elif len(parts) == 2:
            # language_country or language__variant
            language = parts[0]
            second = parts[1]
            if len(language) == 2 and language.isalpha() and language.islower():
                if len(second) == 0:
                    # language__variant (empty country) is not valid with exactly two parts
                    # Actually, if second is empty, that means the string ended with '_'? 
                    # split('_') on 'fr__POSIX' gives ['fr', '', 'POSIX'] -> len 3.
                    # So len(parts)==2 means second is non-empty.
                    # So we need to check if second is all uppercase (country) or not (variant).
                    # But country must be exactly 2 letters? In Java Locale, country is uppercase letters, can be 2 or 3.
                    # We'll follow original: country is 2 uppercase letters.
                    if len(second) == 2 and second.isalpha() and second.isupper():
                        return Locale(language, second)
                    else:
                        # treat as variant? Actually format language_variant is not standard.
                        # The original code only allowed language_country (5 chars) or language_country_variant.
                        # But we need to support language__variant (double underscore).
                        # That case yields parts = ['fr', '', 'POSIX'] -> len 3.
                        # So len(parts)==2 is ambiguous: could be language_country (en_US) or language_variant (en_POSIX).
                        # However, Java's Locale constructor expects country to be uppercase, variant can be anything.
                        # The original method expected length 5 for language_country, so we can check length.
                        # Let's adopt a more robust approach: parse sequentially.
                        pass
                else:
                    # second is non-empty
                    if len(second) == 2 and second.isalpha() and second.isupper():
                        return Locale(language, second)
                    else:
                        # treat as variant (country empty)
                        return Locale(language, "", second)
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        elif len(parts) == 3:
            # language_country_variant or language__variant (empty country)
            language = parts[0]
            country = parts[1]
            variant = parts[2]
            if len(language) == 2 and language.isalpha() and language.islower():
                if len(country) == 0:
                    # language__variant
                    return Locale(language, "", variant)
                else:
                    if len(country) == 2 and country.isalpha() and country.isupper():
                        return Locale(language, country, variant)
                    else:
                        raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")
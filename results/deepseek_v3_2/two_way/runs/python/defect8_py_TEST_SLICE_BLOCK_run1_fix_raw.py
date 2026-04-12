    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if len(parts) == 1:
            # Only language
            language = parts[0]
            if len(language) == 2 and language.isalpha() and language.islower():
                return Locale(language, "")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        elif len(parts) == 2:
            # language and country, or language and variant (if country empty)
            language = parts[0]
            second = parts[1]
            if len(language) == 2 and language.isalpha() and language.islower():
                if len(second) == 0:
                    # language and empty country (e.g., "fr__"? but split yields ['fr', ''])
                    # Actually, split on '_' for "fr__POSIX" yields ['fr', '', 'POSIX']
                    # So len(parts) would be 3. So this case might not happen.
                    # But handle anyway: treat as language only with empty country.
                    return Locale(language, "")
                elif len(second) == 2 and second.isalpha() and second.isupper():
                    # language and country
                    return Locale(language, second)
                else:
                    # second could be variant if country empty? Not with split len=2.
                    # Actually, if country empty and variant present, split yields three parts.
                    # So second is either country or variant? In Java Locale, country is two letters.
                    # So we treat as variant only if country empty? But we need to know.
                    # Better to follow original logic: after language, next part must be country if present.
                    # So we need to parse with underscores, not just split.
                    pass
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        elif len(arts) == 3:
            language = parts[0]
            country = parts[1]
            variant = parts[2]
            if len(language) == 2 and language.isalpha() and language.islower():
                if len(country) == 0 or (len(country) == 2 and country.isalpha() and country.isupper()):
                    return Locale(language, country, variant)
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")
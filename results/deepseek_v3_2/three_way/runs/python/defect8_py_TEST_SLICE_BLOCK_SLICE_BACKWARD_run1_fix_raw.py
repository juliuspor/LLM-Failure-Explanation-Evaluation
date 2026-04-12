    @classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        
        parts = locale_str.split('_')
        if len(parts) == 1:
            # language only
            language = parts[0]
            if len(language) == 2:
                if not language.isalpha() or not language.islower():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(language, "")
            else:
                # ISO 639 alpha-3 language code?
                # Accept any language code that is all lowercase letters
                if not language.isalpha() or not language.islower():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(language, "")
        elif len(parts) == 2:
            # language and country, or language and variant (if country empty)
            language = parts[0]
            second = parts[1]
            if len(language) < 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if len(second) == 2 and second.isalpha() and second.isupper():
                # second is a country code
                return Locale(language, second)
            else:
                # second is a variant, country is empty
                # language must be valid (already checked)
                return Locale(language, "", second)
        elif len(parts) == 3:
            # language, country, variant (country may be empty)
            language = parts[0]
            country = parts[1]
            variant = parts[2]
            if len(language) < 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if country == "":
                # empty country is allowed
                pass
            elif len(country) == 2 and country.isalpha() and country.isupper():
                # valid country code
                pass
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
        else:
            # more than three parts? Not standard, but we can treat extra parts as part of variant
            language = parts[0]
            country = parts[1] if len(parts[1]) > 0 else ""
            variant = '_'.join(parts[2:])
            if len(language) < 2 or not language.isalpha() or not language.islower():
                raise ValueError(f"Invalid locale format: {locale_str}")
            if country == "":
                pass
            elif len(country) == 2 and country.isalpha() and country.isupper():
                pass
            else:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country, variant)
@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # language must be 2-8 chars
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # split by underscores up to 3 parts
        parts = locale_str.split('_')
        if len(parts) == 1:
            language = parts[0]
            country = ""
            variant = ""
        elif len(parts) == 2:
            language, country = parts
            variant = ""
        else:
            # join any remaining underscores into variant
            language = parts[0]
            country = parts[1]
            variant = '_'.join(parts[2:])

        # validate language: 2-8 lowercase letters
        if not (2 <= len(language) <= 8) or not language.isalpha() or not language.islower():
            raise ValueError(f"Invalid locale format: {locale_str}")

        # validate country: empty OR 2 uppercase letters OR 3 digits
        if country:
            if not ((len(country) == 2 and country.isalpha() and country.isupper()) or
                    (len(country) == 3 and country.isdigit())):
                raise ValueError(f"Invalid locale format: {locale_str}")

        # validate variant: if present must be non-empty
        if variant is not None and len(variant) == 0 and len(parts) > 2:
            # explicit empty variant (e.g., "en_US_") is invalid
            raise ValueError(f"Invalid locale format: {locale_str}")

        return Locale(language, country, variant)
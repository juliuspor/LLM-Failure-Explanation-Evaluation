@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        parts = locale_str.split('_', 2)
        # Validate language
        if len(parts[0]) != 2 or not parts[0].islower() or not parts[0].isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")

        language = parts[0]

        if len(parts) == 1:
            return Locale(language, "")
        elif len(parts) == 2:
            country = parts[1]
            if country == "":
                # language_ (trailing underscore with empty country) is invalid
                raise ValueError(f"Invalid locale format: {locale_str}")
            # country must be two uppercase letters
            if len(country) != 2 or not country.isupper() or not country.isalpha():
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country)
        else:
            # Three parts: language, country (maybe empty), variant
            country = parts[1]
            variant = parts[2]
            if country == "":
                # Pattern language__variant
                if variant == "":
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(language, "", variant)
            else:
                # country must be two uppercase letters
                if len(country) != 2 or not country.isupper() or not country.isalpha():
                    raise ValueError(f"Invalid locale format: {locale_str}")
                if variant == "":
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(language, country, variant)
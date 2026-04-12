@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        # Basic length checks: allow 2 (language), 5 (language_country),
        # or >=7 (language_country_variant or language__variant)
        length = len(locale_str)
        if length != 2 and length != 5 and length < 7:
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Split into parts by underscore to handle empty country (e.g., 'fr__POSIX')
        parts = locale_str.split('_')

        # Validate language
        if len(parts[0]) != 2 or not parts[0].islower() or not parts[0].isalpha():
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]

        # No underscore at all -> just language
        if len(parts) == 1:
            return Locale(language, "")

        # If there is only one underscore at end or empty variant, it's invalid
        # e.g., 'en_' or 'en_GB_' are invalid
        # Handle country and variant depending on parts
        # Possible splits:
        # [lang, country]
        # [lang, '', variant]  -> empty country
        # [lang, country, variant]
        # If more than 3 parts, variant may contain underscores; recombine
        if len(parts) >= 3:
            # country may be empty string
            country = parts[1]
            variant = '_'.join(parts[2:])
        else:
            country = parts[1]
            variant = ""

        # Validate country: either empty or two uppercase letters
        if country != "":
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")

        # If variant present, ensure it's non-empty
        if variant == "":
            if country == "":
                # Cases like 'en__' or 'en_' are invalid
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country)
        else:
            return Locale(language, country, variant)
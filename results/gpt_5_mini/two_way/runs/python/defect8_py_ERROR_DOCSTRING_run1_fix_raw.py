@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        # Split into parts to handle empty country (e.g., 'fr__POSIX')
        parts = locale_str.split('_')
        # Validate language
        if len(parts) == 0 or len(parts[0]) < 2 or len(parts[0]) > 8:
            raise ValueError(f"Invalid locale format: {locale_str}")
        language = parts[0]
        if not (len(language) == 2 and 'a' <= language[0] <= 'z' and 'a' <= language[1] <= 'z'):
            # Allow general check for 2-letter lowercase languages as original
            raise ValueError(f"Invalid locale format: {locale_str}")
        # No more parts -> language only
        if len(parts) == 1:
            return Locale(language, "")
        # There is at least a country (which may be empty) or variant
        country = parts[1]
        # If only two parts and country non-empty -> language_country
        if len(parts) == 2:
            if country == "":
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not ((len(country) == 2 and country.isupper()) or (len(country) == 3 and country.isdigit())):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(language, country)
        # len(parts) >=3 => variant present, country may be empty
        variant = '_'.join(parts[2:]) if len(parts) > 3 else parts[2]
        # Validate country if non-empty
        if country != "":
            if not ((len(country) == 2 and country.isupper()) or (len(country) == 3 and country.isdigit())):
                raise ValueError(f"Invalid locale format: {locale_str}")
        # Validate variant when present: must be non-empty
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)
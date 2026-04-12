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
            # second part could be country or variant if country is empty
            if len(parts[1]) == 0:
                # empty country, e.g., "fr__POSIX"
                country = ""
                if len(parts) >= 3:
                    variant = parts[2]
                else:
                    # only one underscore? e.g., "fr_"? treat as empty country, no variant
                    variant = ""
            else:
                # second part non-empty
                if len(parts[1]) == 2 and parts[1].isalpha() and parts[1].isupper():
                    country = parts[1]
                    if len(parts) >= 3:
                        variant = parts[2]
                else:
                    # second part is not a valid country code, treat as variant
                    country = ""
                    variant = parts[1]
                    # if there are more parts, join them as variant? but spec says only one variant.
                    # For simplicity, join remaining parts with underscore.
                    if len(parts) > 2:
                        variant = '_'.join(parts[1:])
        # Validate country if present
        if country and (len(country) != 2 or not country.isalpha() or not country.isupper()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)
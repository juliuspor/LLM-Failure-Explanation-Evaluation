@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # Accept language (2), language_country (5), or language_country_variant (>=7)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")

        ch0 = locale_str[0]
        ch1 = locale_str[1]
        if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 2:
            return Locale(locale_str, "")

        # From here on we expect an underscore at position 2
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Handle language + '_' + country (2 letters) or language + '__' + variant
        # Ensure there are at least 5 chars for a country (e.g., en_US)
        if length == 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
            if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])

        # For lengths >=7 we can have either en__variant (empty country) or en_US_variant
        if length >= 7:
            # If country is empty, positions 3 and 4 should be '_' and variant starts at 5
            if locale_str[3] == '_' and locale_str[4] == '_':
                # variant must exist
                if length == 5:
                    # would have been handled above, but guarded
                    return Locale(locale_str[0:2], "")
                # variant starts at index 5
                variant = locale_str[5:]
                if len(variant) == 0:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], "", variant)
            else:
                # Expect country at positions 3 and 4 as uppercase letters
                ch3 = locale_str[3]
                ch4 = locale_str[4]
                if ch3 < 'A' or ch3 > 'Z' or ch4 < 'A' or ch4 > 'Z':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                # Next must be underscore separating variant
                if locale_str[5] != '_':
                    raise ValueError(f"Invalid locale format: {locale_str}")
                variant = locale_str[6:]
                if len(variant) == 0:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], locale_str[3:5], variant)

        raise ValueError(f"Invalid locale format: {locale_str}")
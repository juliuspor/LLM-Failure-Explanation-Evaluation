@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # Valid forms: ll, ll_CC, ll_CC_variant where ll lowercase, CC uppercase
        if length < 2:
            raise ValueError(f"Invalid locale format: '{locale_str}' (length={length})")

        # First two chars must be lowercase letters
        if length < 2 or not (locale_str[0].islower() and locale_str[1].islower() and locale_str[0].isalpha() and locale_str[1].isalpha()):
            raise ValueError(f"Invalid locale format: '{locale_str}' (language must be two lowercase letters)")

        if length == 2:
            return Locale(locale_str, "")

        # Must have underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: '{locale_str}' (expected '_')")

        # Ensure we have at least two chars for country
        if length < 5:
            raise ValueError(f"Invalid locale format: '{locale_str}' (country missing or too short)")

        country = locale_str[3:5]
        if not (country[0].isupper() and country[1].isupper() and country[0].isalpha() and country[1].isalpha()):
            raise ValueError(f"Invalid locale format: '{locale_str}' (country must be two uppercase letters)")

        if length == 5:
            return Locale(locale_str[0:2], country)

        # length > 5, expect another underscore before variant
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: '{locale_str}' (expected '_' before variant)")

        variant = locale_str[6:]
        return Locale(locale_str[0:2], country, variant)
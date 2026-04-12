@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None

        length = len(locale_str)
        # Accept length 2 (language), 5 (language_COUNTRY), or >=7 (language_COUNTRY_variant)
        if length == 2:
            # Validate language is lowercase letters
            if not (locale_str[0].islower() and locale_str[0].isalpha() and
                    locale_str[1].islower() and locale_str[1].isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")

        if length == 5:
            # Expect pattern ll_CC
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not (locale_str[0].islower() and locale_str[0].isalpha() and
                    locale_str[1].islower() and locale_str[1].isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not (locale_str[3].isupper() and locale_str[3].isalpha() and
                    locale_str[4].isupper() and locale_str[4].isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])

        if length >= 7:
            # Expect pattern ll_CC_variant where underscores at 2 and 5
            if locale_str[2] != '_' or locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not (locale_str[0].islower() and locale_str[0].isalpha() and
                    locale_str[1].islower() and locale_str[1].isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not (locale_str[3].isupper() and locale_str[3].isalpha() and
                    locale_str[4].isupper() and locale_str[4].isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], variant)

        # Any other lengths (3 or 4) are invalid
        raise ValueError(f"Invalid locale format: {locale_str}")
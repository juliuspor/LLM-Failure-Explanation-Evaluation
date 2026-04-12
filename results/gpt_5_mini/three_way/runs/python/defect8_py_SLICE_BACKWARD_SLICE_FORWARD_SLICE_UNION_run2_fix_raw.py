@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # basic validation: minimum 2 chars for language
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # language must be two lowercase letters
        if not (locale_str[0].islower() and locale_str[0].isalpha() and
                locale_str[1].islower() and locale_str[1].isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        # language only (e.g., "en")
        if length == 2:
            return Locale(locale_str[0:2], "")
        # must have separator after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # country form (e.g., "en_GB") -> total length == 5
        if length == 5:
            # validate country two uppercase letters
            if not (locale_str[3].isupper() and locale_str[3].isalpha() and
                    locale_str[4].isupper() and locale_str[4].isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])
        # variant form requires at least 7 characters: ll_CC_v or longer
        if length >= 7:
            # positions 3 and 4 must be country uppercase letters
            if not (locale_str[3].isupper() and locale_str[3].isalpha() and
                    locale_str[4].isupper() and locale_str[4].isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            # separator before variant
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            variant = locale_str[6:]
            if len(variant) == 0:
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], variant)
        # any other length is invalid
        raise ValueError(f"Invalid locale format: {locale_str}")
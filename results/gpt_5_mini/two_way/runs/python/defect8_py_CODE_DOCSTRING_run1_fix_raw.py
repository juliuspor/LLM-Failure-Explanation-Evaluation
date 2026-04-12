@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # valid forms: 2 (ll), 5 (ll_CC), >=7 (ll_CC_variant)
        if length == 2:
            if not (locale_str[0].islower() and locale_str[1].islower()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str, "")
        if length == 5:
            if locale_str[2] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not (locale_str[0].islower() and locale_str[1].islower() and
                    locale_str[3].isupper() and locale_str[4].isupper()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])
        if length >= 7:
            # form ll_CC_variant where variant may contain underscores
            if locale_str[2] != '_' or locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if not (locale_str[0].islower() and locale_str[1].islower() and
                    locale_str[3].isupper() and locale_str[4].isupper()):
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
        # any other lengths (e.g., 0,1,3,4,6) are invalid
        raise ValueError(f"Invalid locale format: {locale_str}")
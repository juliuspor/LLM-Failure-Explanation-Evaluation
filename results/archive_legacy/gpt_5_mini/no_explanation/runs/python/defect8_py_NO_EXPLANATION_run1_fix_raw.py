@classmethod
    def to_locale(cls, locale_str: str) -> Optional[Locale]:
        if locale_str is None:
            return None
        length = len(locale_str)
        # Valid forms: ll | ll_CC | ll_CC_Variant (where ll lowercase, CC uppercase)
        if length < 2:
            raise ValueError(f"Invalid locale format: {locale_str}")
        # check language
        if length >= 2:
            lang = locale_str[0:2]
            if not (lang[0].islower() and lang[1].islower() and lang.isalpha()):
                raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 2:
            return Locale(lang, "")
        # must have underscore after language
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        # check for country
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        country = locale_str[3:5]
        if not (country[0].isupper() and country[1].isupper() and country.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")
        if length == 5:
            return Locale(lang, country)
        # there is a variant: must have underscore at pos 5
        if locale_str[5] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")
        variant = locale_str[6:]
        if len(variant) == 0:
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(lang, country, variant)
@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None
    length = len(locale_str)
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = locale_str[0:2]
    if len(language) != 2 or not language.isalpha() or not language.islower():
        raise ValueError(f"Invalid locale format: {locale_str}")
    if length == 2:
        return Locale(language, "")
    if locale_str[2] != '_':
        raise ValueError(f"Invalid locale format: {locale_str}")
    rest = locale_str[3:]
    if rest == "":
        return Locale(language, "")
    second_underscore = rest.find('_')
    if second_underscore == -1:
        country = rest
        if len(country) != 2 or not country.isalpha() or not country.isupper():
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country)
    else:
        country = rest[:second_underscore]
        variant = rest[second_underscore+1:]
        if country != "":
            if len(country) != 2 or not country.isalpha() or not country.isupper():
                raise ValueError(f"Invalid locale format: {locale_str}")
        if variant == "":
            raise ValueError(f"Invalid locale format: {locale_str}")
        return Locale(language, country, variant)
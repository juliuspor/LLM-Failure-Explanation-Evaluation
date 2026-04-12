@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    import re
    if locale_str is None:
        return None

    # Accept forms: ll, ll_CC, ll_CC_VARIANT, ll__VARIANT (empty country)
    # language: 2 lowercase letters
    # country: 2 uppercase letters (optional, may be empty when two underscores used)
    # variant: one or more alphanumeric or underscore characters
    pattern = re.compile(r'^[a-z]{2}(?:_([A-Z]{2}|) (?:_(.+))?|)$'.replace(' ', ''))
    m = pattern.match(locale_str)
    if not m:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # m.groups(): (country_or_empty, variant_or_none)
    country = m.group(1)
    variant = m.group(2)

    if country is None and variant is None:
        # only language
        return Locale(locale_str, "")
    if variant is None:
        # language + country (country may be empty string if matched)
        return Locale(locale_str[0:2], country or "")
    # language + country (possibly empty) + variant
    return Locale(locale_str[0:2], country or "", variant)

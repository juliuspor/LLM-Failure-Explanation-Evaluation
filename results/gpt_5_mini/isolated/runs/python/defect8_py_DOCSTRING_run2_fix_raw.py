@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    import re
    # Language: 2-3 lowercase letters. Country: 2 uppercase letters. Variant: one or more word chars or any non-empty sequence excluding leading underscore.
    pattern = re.compile(r'^(?P<lang>[a-z]{2,3})(?:_(?P<country>[A-Z]{2}))?(?:_(?P<variant>.+))?$')
    m = pattern.match(locale_str)
    if not m:
        raise ValueError(f"Invalid locale format: {locale_str}")

    lang = m.group('lang')
    country = m.group('country') or ""
    variant = m.group('variant') or ""

    # Additional sanity: prevent empty country when underscore present (e.g., 'en_') is already handled by regex.
    return Locale(lang, country, variant)

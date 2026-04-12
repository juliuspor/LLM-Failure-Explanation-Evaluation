@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    # Accept both '_' and '-' as separators, prefer '_' by replacing '-'
    ls = locale_str.replace('-', '_')
    parts = ls.split('_')

    # Language must be present and 2 letters
    if len(parts) == 0 or len(parts[0]) != 2 or not parts[0].isalpha():
        raise ValueError(f"Invalid locale format: {locale_str}")
    language = parts[0].lower()

    # No further parts -> language only
    if len(parts) == 1:
        return Locale(language, "")

    # If there are two parts, could be language_country or language__variant (empty country)
    country = ""
    variant = ""

    if len(parts) >= 2:
        # parts[1] may be country (2 letters) or empty (meaning variant follows)
        p1 = parts[1]
        if p1 == "":
            country = ""
        else:
            # Country should be 2 letters or 3-digit numeric (UN M.49)
            if (len(p1) == 2 and p1.isalpha()) or (len(p1) == 3 and p1.isdigit()):
                country = p1.upper()
            else:
                # If it's longer, treat as invalid country unless it's actually the start of a variant
                # e.g. 'fr_POSIX' should be interpreted as country='POSIX' is invalid, so treat as variant with empty country
                # Therefore, if p1.isalpha() and len(p1) > 2, treat as variant and leave country empty
                if p1.isalpha():
                    # treat as variant, shift
                    country = ""
                    variant = '_'.join(parts[1:])
                    return Locale(language, country, variant)
                else:
                    raise ValueError(f"Invalid locale format: {locale_str}")

    # If there are more than 2 parts, the rest is variant
    if len(parts) >= 3:
        variant = '_'.join(parts[2:])

    return Locale(language, country, variant)
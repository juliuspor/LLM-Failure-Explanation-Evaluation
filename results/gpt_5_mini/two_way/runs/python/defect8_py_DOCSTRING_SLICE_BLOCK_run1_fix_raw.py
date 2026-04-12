@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length != 2 and length != 5 and length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")

    # Validate language (positions 0-1) must be letters a-z or A-Z
    if length < 2:
        raise ValueError(f"Invalid locale format: {locale_str}")
    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if not (ch0.isalpha() and ch1.isalpha()):
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")
    else:
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # Validate country (positions 3-4) must be letters
        ch3 = locale_str[3]
        ch4 = locale_str[4]
        if not (ch3.isalpha() and ch4.isalpha()):
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 5:
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
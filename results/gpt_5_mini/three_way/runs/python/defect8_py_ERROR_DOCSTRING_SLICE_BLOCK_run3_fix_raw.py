@classmethod
def to_locale(cls, locale_str: str) -> Optional[Locale]:
    if locale_str is None:
        return None

    length = len(locale_str)
    if length != 2 and length != 5 and length < 7:
        raise ValueError(f"Invalid locale format: {locale_str}")

    ch0 = locale_str[0]
    ch1 = locale_str[1]
    if ch0 < 'a' or ch0 > 'z' or ch1 < 'a' or ch1 > 'z':
        raise ValueError(f"Invalid locale format: {locale_str}")

    if length == 2:
        return Locale(locale_str, "")
    else:
        if locale_str[2] != '_':
            raise ValueError(f"Invalid locale format: {locale_str}")

        # region may be two uppercase letters or empty (represented by two underscores)
        # Ensure there are at least 5 characters to access ch3 and ch4
        if length < 5:
            raise ValueError(f"Invalid locale format: {locale_str}")

        ch3 = locale_str[3]
        ch4 = locale_str[4]

        is_empty_country = (ch3 == '_' and ch4 == '_')
        is_valid_country = (ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z')

        if not (is_empty_country or is_valid_country):
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 5:
            # if country is empty (e.g. 'fr__'), treat as language only
            if is_empty_country:
                return Locale(locale_str[0:2], "")
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            # if country is empty (fr__POSIX), variant starts at pos6 and country is empty
            if is_empty_country:
                return Locale(locale_str[0:2], "", locale_str[6:])
            return Locale(locale_str[0:2], locale_str[3:5], locale_str[6:])
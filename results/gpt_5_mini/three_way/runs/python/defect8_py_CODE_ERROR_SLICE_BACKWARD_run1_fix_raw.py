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

        # Possible forms now:
        # ll_CC
        # ll_CC_variant
        # ll__variant (empty country)
        # Validate country part: either two uppercase letters or two underscores
        if length >= 5:
            ch3 = locale_str[3]
            ch4 = locale_str[4]
        else:
            raise ValueError(f"Invalid locale format: {locale_str}")

        country_is_empty = (ch3 == '_' and ch4 == '_')
        country_is_code = (ch3 >= 'A' and ch3 <= 'Z' and ch4 >= 'A' and ch4 <= 'Z')

        if not country_is_empty and not country_is_code:
            raise ValueError(f"Invalid locale format: {locale_str}")

        if length == 5:
            if country_is_empty:
                # form 'll__' is invalid (no variant)
                raise ValueError(f"Invalid locale format: {locale_str}")
            return Locale(locale_str[0:2], locale_str[3:5])
        else:
            # length >= 7, must have underscore at position 5 separating variant
            if locale_str[5] != '_':
                raise ValueError(f"Invalid locale format: {locale_str}")
            if country_is_empty:
                # variant starts at position 4 (since positions 2 and 3 are '_')? Actually ll__variant => underscores at 2 and 3?
                # Given indexes: 0-1 language, 2 '_', 3 '_', 4 is start of variant in this scenario
                # But our country_is_empty checks ch3== '_' and ch4=='_', meaning indexes 3 and 4 are underscores. That shifts variant to start at 5.
                # Correct mapping: For ll__variant, positions: 0-1 ll, 2 '_', 3 '_', 4 start of variant -> however original Java expects ll__variant where variant starts at index 4.
                # To support common formats, accept variant starting at index 6 as original code did for ll_CC_variant and index 4 for ll__variant.
                # Determine variant start: if ch3 == '_' and ch4 == '_', variant = locale_str[4:]
                variant = locale_str[4:]
                if len(variant) == 0:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], "", variant)
            else:
                # normal ll_CC_variant where variant starts at index 6
                variant = locale_str[6:]
                if len(variant) == 0:
                    raise ValueError(f"Invalid locale format: {locale_str}")
                return Locale(locale_str[0:2], locale_str[3:5], variant)